from flask import Flask, request, jsonify
from rabbit import RabbitMQ
import time


app = Flask(__name__)
rabbit = RabbitMQ('chat_queue')

time.sleep(10)
rabbit.start_consuming()  # Iniciar a thread de consumo

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    rabbit.send_message(message)
    return jsonify({'status': 'Message sent successfully'})

@app.route('/receive_messages', methods=['GET'])
def receive_messages():
    with rabbit.lock:
        messages = list(rabbit.messages)
        rabbit.messages = []  # Limpar as mensagens recebidas
    return jsonify({'messages': messages})