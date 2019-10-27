import json
from flask import Flask
from Models.db__init import db

class FBSendModel(db.Model):
    __tablename__= "fbsend"
    userId = db.Column(db.String(1024), primary_key=True)
    pageLink = db.Column(db.String(65535))
    message = db.Column(db.String(65535))
    is_sent = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, userId, pageLink="", message=""):
        self.userId = userId
        self.pageLink = pageLink
        self.message = message

    def __repr__(self):
        return '<FBSendModel | FBSendModel %r>' % self.token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_without_sent(self):
        return self.query.filter_by(is_sent=False).all()

    @property
    def data(self):
        return {
            "userId": self.userId,
            "pageLink": self.pageLink
        }