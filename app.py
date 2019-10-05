from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from swagger_ui import flask_api_doc
from config import config
from Controllers.Product import *
from Controllers.Cart import *
from Models.db__init import db_init, db

app = Flask(__name__)
CORS(app)
app.config.from_object(config['default'])
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db_init(app)
api = Api(app)

flask_api_doc(app, config_path='./api.yaml', url_prefix='/api/v1/doc', title='API doc')

class APIDocs(Resource):
    def get(self):
        return {
            "version": "1.0.0"
        }
        
@app.route("/")
def hello():
    return "Hello! Do not try to spy me!"

api.add_resource(APIDocs, '/api/', '/api/v1/')
api.add_resource(Product, '/api/v1/products', '/api/v1/products/', '/api/v1/products/<string:id>')
api.add_resource(Basket, '/api/v1/basket', '/api/v1/basket/', '/api/v1/basket/<string:id>')
api.add_resource(Checkout, '/api/v1/checkout', '/api/v1/checkout/')
api.add_resource(Complete, '/api/v1/complete', '/api/v1/complete/')

if __name__ == '__main__':
    app.run()