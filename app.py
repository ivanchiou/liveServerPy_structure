from flask import Flask
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from Controllers.Product import *
from Controllers.Cart import *
from Controllers.FB import *
from Models.db__init import db_init, db
from Models.ProductModel import *
from flask_swagger import swagger
from swagger_ui import flask_api_doc
from config import config, auth, cache, USERS_TOKEN

app = Flask(__name__, static_url_path='/static')
cache.init_app(app)
CORS(app)
app.config.from_object(config['default'])
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db_init(app)
api = Api(app)

flask_api_doc(app, config_path='./api.yaml', url_prefix='/api/v1/doc', title='API doc')

class APIDocs(Resource):
    decorators = [auth.login_required]
    @cache.cached(timeout=300, key_prefix='get_apidocs')
    def get(self):
        print("there is no cache")
        return {
            'Products': '商品頁/商品列表頁',
            'Basket': '購物車step1',
            'Checkout': '購物車step2',
            'Complete': '購物車step3'
        }

@auth.verify_password
def verify_password(username, password):
    if username in USERS_TOKEN:
        return check_password_hash(USERS_TOKEN.get(username), password)
    return False

@app.route("/")
@auth.login_required
@cache.cached(timeout=300)
def hello():
    print("there is no cache")
    return "Hello! Do not try to spy me!"

api.add_resource(FBWebhook, '/FBWebhook', '/FBWebhook/') 
api.add_resource(FBLiveComment, '/getLiveVideoComment', '/getLiveVideoComment/')
api.add_resource(FBSendToChat, '/sendToFBChat', '/sendToFBChat/')

@app.route("/spec")
@auth.login_required
@cache.cached(timeout=300)
def spec():
    print("there is no cache")
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Live Server API"    
    return jsonify(swag)

api.add_resource(APIDocs, '/api/', '/api/v1/')
#清空資料庫
with app.app_context():
    try:
        db.create_all()
    except:
        pass
#/api/v1/products/1173626 --- 取得單一商品
#/api/v1/products/   --- 取得所有商品
#/api/v1/products/?cate=34   --- 取得某一分類下的所有商品
api.add_resource(Product, '/api/v1/products', '/api/v1/products/', '/api/v1/products/<string:id>')
# 加入預設資料到資料庫
## 商品列表頁資料
## 購物車資料
cate1 = CategoryDisplayModel(11, "時尚")
cate2 = CategoryDisplayModel(12, "3C")
with app.app_context():
    try:
        cate1.save_to_db()
        cate2.save_to_db()
    except:
        pass


style1 = StyleInfoDisplayModel("a0015", "黑色", 10)
style2 = StyleInfoDisplayModel("a0016", "白色", 6)
with app.app_context():
    try:
        style1.save_to_db()
        style2.save_to_db()
    except:
        pass 

for index in range(12):
    mode = index%2
    product = ProductDisplayModel(index, "Samsung Galaxy S10+ 6.4吋智慧型手機 8G/128G", 10+mode+1, 100*index, image="https://ehs-shop.tyson711.now.sh/static/images/470x600-"+str('{:02}'.format(index+1))+".jpg", styles=["a0015", "a0016"], app=app)
    with app.app_context():
        try:
            product.save_to_db()
        except:
            pass

api.add_resource(Basket, '/api/v1/basket', '/api/v1/basket/', '/api/v1/basket/<string:id>')
api.add_resource(Checkout, '/api/v1/checkout', '/api/v1/checkout/')
api.add_resource(Complete, '/api/v1/complete', '/api/v1/complete/')

if __name__ == '__main__':
    app.run(ssl_context='adhoc')