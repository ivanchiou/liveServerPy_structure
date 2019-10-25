import jwt
import uuid
from datetime import datetime
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from config import auth
from sqlalchemy import and_
from Controllers.Product import *
from Models.UserModel import *
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

domain = "liveserverpy.herokuapp.com"

class Basket(Resource):
    decorators = [auth.login_required]
    def get(self):
        args = parser.parse_args()
        access_token = args['access_token'] if 'access_token' in args else None
        result = []
        if access_token is not None:
            print(access_token)
            try:
                payload = jwt.decode(access_token, 'secret', audience=domain, issuer=domain)
                tokenID = str(payload['jti']) if 'jti' in payload else ''
                print(tokenID)
                user_buy = UserBuyModel.query.filter_by(token=tokenID).all()
                goodIds = []
                stylesIds = []
                quantities = []
                if user_buy is not None:
                    for item in user_buy:
                        data = item.data
                        goodIds.append(data['goodId'])
                        stylesIds.append(data['styleId'])
                        quantities.append(data['quantity'])
                    for index, goodId in enumerate(goodIds):
                        response_json = Product.get(self,goodId)
                        response_json['styleInfo'] = list(filter(lambda data: data['value'] == stylesIds[index], response_json['styleInfo']))[0]
                        response_json['quantity'] = int(quantities[index])
                        result.append(response_json)
            except BaseException as e:
                print('BaseException', e)
                return {
                    'isSuccess': False,
                    'message': e.args
                }                
        return result
        
    def post(self):
        args = parser.parse_args()
        goodId = args['goodId'] if 'goodId' in args else None
        styleId = args['styleId'] if 'styleId' in args and args['styleId'] is not None else ""
        quantity = args['quantity'] if 'quantity' in args and args['quantity'] is not None else 1
        access_token = args['access_token'] if 'access_token' in args else None
        response_json = {
            "isSuccess": False
        }
        if goodId is not None:
            payload = {}
            if access_token is None:
                payload = {
                    'iss': domain,
                    'sub': uuid.uuid1().int>>100,
                    'aud': domain,
                    'exp': datetime.utcnow() + timedelta(seconds=3600),
                    'nbf': datetime.utcnow(),
                    'iat': datetime.utcnow(),
                    'jti': uuid.uuid1().int>>100,
                    'hello': 'world',
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                access_token = token.decode("utf-8")
            else:
                payload = jwt.decode(access_token, 'secret', audience=domain, issuer=domain)
            tokenID = str(payload['jti']) if 'jti' in payload else ''
            user = UserModel.query.filter_by(token=tokenID).first()
            if user is not None:
                search = and_(UserBuyModel.token==tokenID,
                    UserBuyModel.goodId==goodId,
                    UserBuyModel.styleId==styleId
                )
                userbuy = UserBuyModel.query.filter(search).first()
                if userbuy is not None:
                    UserBuyModel.query.filter(search).update({'goodId': goodId, 'styleId': styleId, 'quantity': quantity})
                else:
                    userDB = UserBuyModel(tokenID, goodId, styleId, quantity)
                    userDB.save_to_db()
            else:
                userDB = UserModel(tokenID, goodId, styleId, quantity)
                userDB.save_to_db()
                userBuyDB = UserBuyModel(tokenID, goodId, styleId, quantity)
                userBuyDB.save_to_db()
            response_json['isSuccess'] = True
            response_json['access_token'] = access_token
        else:
            response_json['message'] = "Don't assign correct product goodId"
        return response_json

    def delete(self, id):
        args = parser.parse_args()
        access_token = args['access_token'] if 'access_token' in args else None
        try:
            payload = jwt.decode(access_token, 'secret', audience=domain, issuer=domain)
            tokenID = str(payload['jti']) if 'jti' in payload else ''
            search = and_(UserBuyModel.token==tokenID,
                UserBuyModel.goodId==id
            )            
            userbuy = UserBuyModel.query.filter(search).first()
            if userbuy is not None:
                db.session.delete(userbuy)
                db.session.commit()
                return {
                    'isSuccess': True,
                    'message': 'Successfully Deleted!'
                }
        except:
            pass
        return {
            'isSuccess': False,
            'message': 'Deleted Failed!'
        }

class Checkout(Resource):
    decorators = [auth.login_required]
    def post(self):
        args = parser.parse_args()
        access_token = args['access_token'] if 'access_token' in args else None
        if access_token is not None:
            payload = jwt.decode(access_token, 'secret', audience=domain, issuer=domain)
            tokenID = str(payload['jti']) if 'jti' in payload else ''
            products = args['products'] if 'products' in args else None
            if products is not None:
                goodIds = []
                quantities = []
                total_price = 0
                for index, product in enumerate(products):
                    response_json = Product.get(self,product['goodId'])
                    goodIds.append(str(product['goodId']))
                    quantities.append(str(product['quantity']))
                    total_price += response_json['price']
                receiver = args['receiver']
                payment = args['payment']
                invoice = args['invoice']
                goodIdStr = ','.join(goodIds)
                quantityStr = ','.join(quantities)
                order = OrderDisplayModel(tokenID, goodIdStr, quantityStr, total_price, payment, invoice, receiver)
                order.save_to_db()
                return {
                    "isSuccess": True,
                    "orderId": order.orderId,
                    "message": 'Successfully Checkout!'
                }
            else:
                return {
                    "isSuccess": False,
                    "message": 'There is no products assigned.'
                }
        else:
            return {
                "isSuccess": False,
                "message": 'There is no token assigned.'
            }

class Complete(Resource):
    decorators = [auth.login_required]
    def get(self):
        args = parser.parse_args()
        access_token = args['access_token'] if 'access_token' in args else None
        orderId = args['orderId'] if 'orderId' in args else None
        if access_token is not None and orderId is not None:
            try:
                payload = jwt.decode(access_token, 'secret', audience=domain, issuer=domain)
                tokenID = str(payload['jti']) if 'jti' in payload else ''
                order_model = OrderDisplayModel.query.filter_by(token=tokenID, orderId=orderId).first()
                if order_model is not None:
                    order = order_model.data
                    payment = {}
                    payment["amount"] = order['amount']
                    if order['payment'] == PayementType.ATM.value:
                        payment["bank"] = "永豐銀行"
                        payment["account"] = "20191022019102"
                    UserBuyModel.query.filter_by(token=tokenID).delete()
                    UserModel.query.filter_by(token=tokenID).delete()
                    db.session.commit()
                    return {
                        "order": {
                            "id": order['orderId'],
                            "time": order['timestamp']
                        },
                        "payment": payment
                    }
            except BaseException as e:
                print('BaseException', e)
                return {
                    'isSuccess': False,
                    'message': e.args
                }
            return {
                "isSuccess": False,
                "message": 'There is no order created.'
            }
        else:
            return {
                "isSuccess": False,
                "message": 'There is no token assigned.'
            }