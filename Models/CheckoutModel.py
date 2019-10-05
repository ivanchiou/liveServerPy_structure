import json
from flask import Flask
from Models.db__init import db

class CheckoutProductDisplayModel(db.Model):
    goodId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, goodId, name):
        self.goodId = goodId
        self.name = name

    def __repr__(self):
        return '<CheckoutModel | CheckoutProductDisplayModel %r>' % self.name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, goodId):
        return self.query.filter_by(goodId=goodId).first()

    @property
    def data(self):
        return {
            "goodId": self.goodId,
            "name": self.name
        }