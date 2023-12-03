import pika
import threading

class RabbitMQ:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.messages = []
        self.lock = threading.Lock()

    def consume_messages(self):
        def callback(ch, method, properties, body):
            with self.lock:
                self.messages.append(body.decode())

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))  
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    def start_consuming(self):
        consume_thread = threading.Thread(target=self.consume_messages)
        consume_thread.start()

    def send_message(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')) 
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        connection.close()