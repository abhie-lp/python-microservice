import os
import pika
import django

from json import loads
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

load_dotenv("config.env")


params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare("admin")


def callback(ch, method, properties: pika.BasicProperties, body):
    product_id = loads(body)
    product = Product.objects.get(id=product_id)
    product.likes += 1
    product.save()


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
channel.close()
