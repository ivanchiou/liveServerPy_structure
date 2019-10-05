from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from Models.ProductModel import *
from json import JSONEncoder

parser = reqparse.RequestParser()
parser.add_argument('id')

class Product(Resource):
    # Get Product list
    def get(self, id=None):
        return {
            "isSuccess": True
        }
    
    # Create new product
    def post(self):
        return {
            "isSuccess": True
        }