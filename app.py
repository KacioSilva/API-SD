# backend/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)
user_messages = {}  # Dicionário para armazenar mensagens por usuário

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data.get('user_id')
    message_content = data.get('message')

    if user_id is None or message_content is None:
        return {'status': 'error', 'message': 'User ID and message are required.'}

    if user_id not in user_messages:
        user_messages[user_id] = []

    new_message = {'content': message_content, 'read': False}
    user_messages[user_id].append(new_message)

    return {'status': 'success'}

@app.route('/get_messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    if user_id not in user_messages:
        return {'status': 'error', 'message': 'User not found.'}

    # Recupera as mensagens do usuário
    messages = user_messages[user_id]

    # Marca as mensagens como lidas
    for message in messages:
        message['read'] = True

    # Esvazia a lista de mensagens para o usuário
    user_messages[user_id] = []

    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
