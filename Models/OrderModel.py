import json
import time
import uuid
from flask import Flask
from enum import Enum
from Models.db__init import db

class PayementType(Enum):
    ATM = 0
    COD = 1

class InvoiceType(Enum):
    Donation = 0
    Copies2 = 1

class OrderDisplayModel(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(65536))
    products = db.Column(db.String(65536))
    quantity = db.Column(db.String(65536))
    amount = db.Column(db.Integer)
    receiver_name = db.Column(db.String(65536))
    receiver_phone = db.Column(db.String(65536))
    receiver_addr1 = db.Column(db.String(65536))
    receiver_addr2 = db.Column(db.String(65536))
    payment = db.Column(db.Integer)
    invoice = db.Column(db.Integer)
    timestamp = db.Column(db.String(65536))

    def __init__(self, token, products, quantity, amount, payment, invoice, receiver):
        self.orderId = uuid.uuid1().int>>100
        self.token = token
        self.products = products
        self.quantity = quantity
        self.amount = amount
        self.payment = payment
        self.invoice = invoice
        self.receiver_name = receiver['name']
        self.receiver_phone = receiver['phone']
        self.receiver_addr1 = receiver['addr1']
        self.receiver_addr2 = receiver['addr2']
        self.timestamp = time.time()

    def __repr__(self):
        return '<OrderModel | OrderDisplayModel %r>' % self.orderId

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, orderId):
        return self.query.filter_by(orderId=orderId).first()

    @property
    def data(self):
        return {
            "orderId": self.orderId,
            "amount": self.amount,
            "payment": self.payment,
            "timestamp": self.timestamp
        }