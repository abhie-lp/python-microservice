import os
import pika

from json import loads
from dotenv import load_dotenv
from main import db, Product

load_dotenv("config.env")

params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare("main")


def callback(ch, method: str, properties: pika.BasicProperties, body):
    print("Callback from main")
    data = loads(body)
    print(data)
    
    content_type = properties.content_type.split("_", 1)[1]
    if content_type == "created":
        product = Product(id=data["id"], title=data["title"], image=data["image"])
        db.session.add(product)
        db.session.commit()
    elif content_type == "updated":
        product = Product.query.get(data["id"])
        product.title = data["title"]
        product.image = data["image"]
        db.session.commit()
    elif content_type == "deleted":
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
    else:
        print("Wrong code")
        return


channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=True)

print("STARTED CONSUMING FLASK")
channel.start_consuming()
channel.close()
