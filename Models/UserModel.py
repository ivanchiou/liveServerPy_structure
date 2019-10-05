import json
from flask import Flask
from Models.db__init import db

class UserModel(db.Model):
    __tablename__= "user"
    token = db.Column(db.String(65536), primary_key=True)
    goodId = db.Column(db.String(1024))
    stylesId = db.Column(db.String(1024))
    quantity = db.Column(db.String(1024))

    def __init__(self, token, goodId, stylesId="", quantity=1):
        self.token = token
        self.goodId = goodId
        self.stylesId = stylesId
        self.quantity = quantity

    def __repr__(self):
        return '<UserModel | UserModel %r>' % self.token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, token):
        return self.query.filter_by(token=token).first()

    @property
    def data(self):
        return {
            "token": self.token,
            "goodId": self.goodId,
            "stylesId": self.stylesId,
            "quantity": self.quantity
        }