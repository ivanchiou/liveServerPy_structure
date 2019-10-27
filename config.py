import os
from flask_httpauth import HTTPBasicAuth
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
pjdir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = {
    'user': '',
    'password': '',
    'db': '',
    'host': '',
    'port': '',
}

FB_TOKEN = ''

class Config(object):
    pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    DEBUG = False
    ENV = "production"

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(pjdir, 'data.sqlite')
    DEBUG = True
    ENV = "development"

config = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}

USERS_TOKEN = {
    "Ivan": generate_password_hash("xxx"),
    "Tyson": generate_password_hash("xxx")
}

auth = HTTPBasicAuth()
cache = Cache(config={'CACHE_TYPE': 'simple'})