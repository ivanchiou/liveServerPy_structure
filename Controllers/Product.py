from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from config import auth, cache
from Models.ProductModel import *
from json import JSONEncoder

parser = reqparse.RequestParser()
parser.add_argument('cate')

class ProductObj:
    def __init__(self, goodId):
        self.product = ProductDisplayModel.query.filter_by(goodId=goodId).first().data
        styles = self.product['stylesId'].split(",")
        del self.product['stylesId']
        self.product['styleInfo'] = []
        for index in range(len(styles)):
            style = db.session.query(StyleInfoDisplayModel).filter_by(styleId=styles[index]).first().data
            self.product['styleInfo'].append(style)
    
class ProductObjs:
    def __init__(self):
        self.products = {}
    
    def get_product(self, goodId):
        if goodId not in self.products:
            self.products[goodId] = ProductObj(goodId).product
        return self.products[goodId].copy()

productObjs = ProductObjs()
class Product(Resource):
    decorators = [auth.login_required]
    # 取得商品(列表)資料
    def get(self, id=None):
        args = parser.parse_args()
        goodId = id
        cateId = args['cate'] if 'cate' in args else None
        result = []
        products = []
        if goodId is None:
            result = self.getAllProducts(cateId)
        else:
            result = productObjs.get_product(goodId)
        return result
    
    @cache.cached(timeout=300)
    def getAllProducts(self, cateId):
        print("there is no cache")
        result = []
        if cateId is None:
            products = ProductDisplayModel.query.order_by(ProductDisplayModel.goodId).all()
        else:
            products = ProductDisplayModel.query.filter_by(cateId=cateId).order_by(ProductDisplayModel.goodId).all()
        for product in products:
            is_new_object = True
            if product is None:
                pass
            else:
                current_cate_name = product.get_cate_name_by_id(product.cateId)
                if current_cate_name == None:
                    pass
                else:
                    for item in result:
                        jsonObj = item
                        if 'category' in item and item['category'] == current_cate_name and 'data' in item:
                            item['data'].append(product.data)
                            is_new_object = False
                    if is_new_object:
                        jsonObj = {
                            'category': current_cate_name,
                            'cateId': product.cateId,
                            'data': [product.data]
                        }
                        result.append(jsonObj)
        return result

    # 新增商品
    def post(self):
        json_data = request.get_json(force=True)
        products = json_data['producs']
        return jsonify(products=products)