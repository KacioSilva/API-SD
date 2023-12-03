from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chat_dados_user:fuWlIngju6yUpkZdrSC1r5yIKDRYstOi@dpg-clm00tsjtl8s73eqv2g0-a/chat_dados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    read = db.Column(db.Boolean, default=False)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data.get('user_id')
    message_content = data.get('message')

    if user_id is None or message_content is None:
        return {'status': 'error', 'message': 'ID de usuário e mensagem são obrigatórios.'}

    new_message = Message(user_id=user_id, content=message_content, read=False)

    try:
        db.session.add(new_message)
        db.session.commit()
        return {'status': 'successo'}
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {'status': 'erro'}

@app.route('/get_messages_unread/<user_id>', methods=['GET'])
def get_messages_unread(user_id):
    messages = Message.query.filter_by(user_id=user_id, read=False).all()

    for message in messages:
        message.read = True  # Marca as mensagens como lidas

    db.session.commit()

    return jsonify([{'ID da Mensagem': msg.id, 'Mensagem': f'{msg.content}' } for msg in messages])

@app.route('/get_all_messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    
    messages = Message.query.filter_by(user_id=user_id).all()

    for message in messages:
        message.read = True
        db.session.commit() # Marca as mensagens como lidas

    return jsonify([{'ID da Mensagem': msg.id, 'Mensagem': f'{msg.content}' } for msg in messages])

@app.route('/delete_message/<message_id>', methods=['GET'])
def delete_message(message_id):
    # Busca a mensagem pelo ID
    message = Message.query.get(message_id)

    if message:
        # Se a mensagem existe
        db.session.delete(message)
        db.session.commit()
        return {'status': 'success', 'message': 'A mensagem foi apagada com sucesso!'}
    else:
        # Se a mensagem não existe
        return abort(404, 'A mensagem procurada não é existente')
    
if __name__ == '__main__':
    app.run(debug=True)