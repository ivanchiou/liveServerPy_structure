import json
import uuid
from flask import Flask
from Models.db__init import db

class ProductDisplayModel(db.Model):
    __tablename__= "product"
    goodId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer)
    promoMsg = db.Column(db.String(80))
    image = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    description = db.Column(db.String(1024))
    cateId = db.Column(db.Integer,nullable=True)
    stylesId = db.Column(db.String(80), nullable=True)

    def __init__(self, goodId, name, cateId=None, price=0, promoMsg="30% OFF", image="", url="", description="This is description", styles=[], app=None):
        self.goodId = goodId
        self.name = name
        self.price = price
        self.promoMsg = promoMsg
        self.image = image
        self.url = url
        self.description = description
        self.cateId = cateId
        self.stylesId = ','.join(styles)

    def __repr__(self):
        return '<ProductModel | ProductDisplayModel %r>' % self.name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        return {
            "goodId": self.goodId,
            "name": self.name,
            "price": self.price,
            "promoMsg": self.promoMsg,
            "image": self.image,
            "url": self.url,
            "description": self.description,
            "stylesId": self.stylesId
        }