import json
import uuid
from flask import Flask
from Models.db__init import db

class CategoryDisplayModel(db.Model):
    __tablename__= "category"
    cateId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    product_display = db.relationship('ProductDisplayModel', backref='category', lazy='dynamic')

    def __init__(self, cateId, title):
        self.cateId = cateId
        self.title = title

    def __repr__(self):
        return '<ProductModel | CategoryDisplayModel %r>' % self.title

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, cateId):
        return self.query.filter_by(cateId=cateId).first()

    @property
    def data(self):
        return {
            "cateId": self.cateId,
            "title": self.title
        }

class StyleInfoDisplayModel(db.Model):
    __tablename__= "styleInfo"
    styleId = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(80))
    quantity = db.Column(db.Integer)

    def __init__(self, styleId, title, quantity):
        self.styleId = styleId
        self.title = title
        self.quantity = quantity

    def __repr__(self):
        return '<ProductModel | StyleInfoDisplayModel %r>' % self.title

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, styleId):
        return self.query.filter_by(styleId=styleId).first()

    @property
    def data(self):
        return {
            "value": self.styleId,
            "title": self.title,
            "quantity": self.quantity
        }

class ProductStyleInfoRelationModel(db.Model):
    styleId = db.Column(db.String(80), db.ForeignKey('styleInfo.styleId'), primary_key=True)
    goodId = db.Column(db.Integer, primary_key=True)

    def __init__(self, styleId, goodId):
        self.styleId = styleId
        self.goodId = goodId

    def __repr__(self):
        return '<ProductModel | ProductStyleInfoRelationModel>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, styleId):
        return self.query.filter_by(styleId=styleId).first()

    @property
    def data(self):
        return {
            "styleId": self.styleId,
            "goodId": self.goodId
        }

class ProductDisplayModel(db.Model):
    __tablename__= "product"
    goodId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer)
    promoMsg = db.Column(db.String(80))
    image = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    description = db.Column(db.String(1024))
    cateId = db.Column(db.Integer, db.ForeignKey('category.cateId'), nullable=True)

    def __init__(self, goodId, name, cateId=None, price=0, promoMsg="30% OFF", image="", url="", description="This is description", styles=[], app=None):
        self.goodId = goodId
        self.name = name
        self.price = price
        self.promoMsg = promoMsg
        self.image = image
        self.url = url
        self.description = description
        self.cateId = cateId
        for index in range(len(styles)):
            try:
                psr = ProductStyleInfoRelationModel(styles[index], goodId)
                if app is not None:
                    with app.app_context():
                        psr.save_to_db()
            except:
                pass

    def __repr__(self):
        return '<ProductModel | ProductDisplayModel %r>' % self.name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def find_by_id(self, goodId):
        return db.session.query.filter_by(goodId=goodId).first()
    
    def get_cate_name_by_id(self, cateId):
        elem_list = db.session.query(CategoryDisplayModel.title).filter_by(cateId=cateId).first()
        return elem_list[0] if len(elem_list) > 0 else None

    @property
    def data(self):
        prodStyles = ProductStyleInfoRelationModel.query.filter_by(goodId=self.goodId).all()
        stylesIds = []
        for item in prodStyles:
            data = item.data
            stylesIds.append(data['styleId'])
        return {
            "goodId": self.goodId,
            "name": self.name,
            "price": self.price,
            "promoMsg": self.promoMsg,
            "image": self.image,
            "url": self.url,
            "description": self.description,
            "stylesId": ','.join(stylesIds)
        }