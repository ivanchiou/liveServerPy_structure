import json
from flask import Flask
from Models.db__init import db
from Models.ProductModel import *

class UserBuyModel(db.Model):
    __tablename__= "userbuy"
    pid = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(65536), db.ForeignKey('user.token'))
    goodId = db.Column(db.Integer, db.ForeignKey('product.goodId'))
    styleId = db.Column(db.String(80), db.ForeignKey('styleInfo.styleId'))
    quantity = db.Column(db.Integer)

    def __init__(self, token, goodId, styleId, quantity=1):
        self.pid = uuid.uuid1().int>>100
        self.token = token
        self.goodId = goodId
        self.styleId = styleId
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
            "styleId": self.styleId,
            "quantity": self.quantity
        }

class UserModel(db.Model):
    __tablename__= "user"
    token = db.Column(db.String(65536), primary_key=True)

    def __init__(self, token, goodId, stylesId="", quantity=1, app=None):
        self.token = token
        goodIdList = list(goodId.split(","))
        styleIdList = list(stylesId.split(","))
        quantityIdList = list(quantity.split(","))
        for index in range(len(goodIdList)):
            op = UserBuyModel(token, goodIdList[index], styleIdList[index], quantityIdList[index])
            if app is not None:
                with app.app_context():
                    op.save_to_db()

    def __repr__(self):
        return '<UserModel | UserModel %r>' % self.token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, token):
        return self.query.filter_by(token=token).first()

    @property
    def data(self):
        userbuy = db.session.query(UserBuyModel).filter_by(token=self.token).all()
        goodIdList = []
        styleIdList = []
        quantityIdList = []
        for item in userbuy:
            data = item.data
            goodIdList.append(data['goodId'])
            styleIdList.append(data['styleId'])
            quantityIdList.append(data['quantity'])
        return {
            "token": self.token,
            "goodId": ','.join(goodIdList),
            "stylesId": ','.join(styleIdList),
            "quantity": ','.join(quantityIdList)
        }