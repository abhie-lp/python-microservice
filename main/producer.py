import os
import pika

from dotenv import load_dotenv
from json import dumps

load_dotenv("config.env")

params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="admin", body=dumps(body),
        properties=properties
    )