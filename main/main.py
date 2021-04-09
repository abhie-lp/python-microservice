from producer import publish
import requests

from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    # Autoincrement is False because product is not created in this app
    # It is created in Django app and maps pk from their
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int

    __table_args__ = (UniqueConstraint(
            "user_id", "product_id", name="user_product_unique"
        ),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)


@app.route("/products/")
def index():
    return jsonify(Product.query.all())


@app.route("/product/<int:id>/like/", methods=["POST"])
def like(id):
    # Call the api to get random user
    req = requests.get("http://docker.for.linux.localhost:8000/user/")
    json = req.json()
    try:
        product_user = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish("product_liked", id)
    except:
        abort(400, "You already liked this product.")
    return jsonify(req.json())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")