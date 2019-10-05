from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class db_init:
    def __init__(self, app):
        global db
        db.init_app(app)