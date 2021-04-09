import os
import pika

from dotenv import load_dotenv

load_dotenv("config.env")

params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare("admin")


def callback(ch, method, properties, body):
    print("Callback from admin")
    print("admin", "hello")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

print("STARTED CONSUMING DJANGO")
channel.start_consuming()
channel.close()
