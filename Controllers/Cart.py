import jwt
from datetime import datetime
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from Controllers.Product import *
from Models.UserModel import *
from Models.CheckoutModel import *
from Models.OrderModel import *
from json import JSONEncoder

parser = reqparse.RequestParser()
parser.add_argument('products', type=list, location='json')
parser.add_argument('receiver', type=dict)
parser.add_argument('goodId')
parser.add_argument('styleId')
parser.add_argument('quantity')
parser.add_argument('payment')
parser.add_argument('invoice')
parser.add_argument('orderId')
parser.add_argument('access_token')

class Basket(Resource):
    def get(self):
        return {
            'isSuccess': False,
            'message': 'Access Denied'
        }
        
    def post(self):
        access_token = args['access_token'] if 'access_token' in args else None
        if access_token is None:
            payload = {
                'iss': 'liveserverpy.herokuapp.com',
                'sub': goodId,
                'aud': 'liveserverpy.herokuapp.com',
                'exp': datetime.utcnow(),
                'nbf': datetime.utcnow(),
                'iat': datetime.utcnow(),
                'jti': goodId,
                'hello': 'world',
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            access_token = token.decode("utf-8")
        return {
            'access_token': access_token
        }           

    def delete(self, id):
        return {
            'isSuccess': False,
            'message': 'Deleted Failed!'
        }


class Checkout(Resource):
    def post(self):
        return {
            "isSuccess": False,
            "message": 'There is no token assigned.'
        }


class Complete(Resource):
    def get(self):
        return {
            "isSuccess": False,
            "message": 'There is no token assigned.'
        }