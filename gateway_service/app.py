from flask import Flask,jsonify,make_response,send_from_directory
from flask_cors import CORS
# from routes import request_api
import argparse
from flask_restful import Api
import time
from flask import g
from resources.user import  UserData,UserList,UserLogin
from resources.product import CategoryData,CategoryList,SingleCategory,ItemData,SingleItem,ItemList,ReduceItemCount
from resources.cashflow import CartData,CartDataList,CartSingleItem,MakePayment,PaymentListUser
from resources.promo import PromoData,PromoList
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.secret_key = 'Lakshya Srivastava Project'
api = Api(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Advanced Python(Flask) present HashKart"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
# app.register_blueprint(request_api.get_blueprint())

#Run on all request
@app.before_request
def before_request_time():
    g.start=time.time()

#Run on all request
@app.after_request
def after_request_time(response):
    time_diff=int((time.time()- g.start)*1000)
    response.headers["X-TIME-TO-EXECUTE"] = f"{time_diff} ms."
    return response

api.add_resource(UserData,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(UserList,'/users')

api.add_resource(CategoryData,'/createCategory')
api.add_resource(SingleCategory,'/category/<string:name>')
api.add_resource(CategoryList,'/categories')
api.add_resource(ItemData,'/newItem')
api.add_resource(SingleItem,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(ReduceItemCount,'/decreaseItemCount/<string:name>/<int:quantity>')

api.add_resource(CartData,'/cartdata')
api.add_resource(CartDataList,'/cartdata')
api.add_resource(CartSingleItem,'/cartdata/<int:product_id>')
api.add_resource(MakePayment,'/makePayment')
api.add_resource(PaymentListUser,'/myPayments')

api.add_resource(PromoData,'/promodata/<string:name>')
api.add_resource(PromoList,'/promolist')

if __name__=='__main__':
    app.run(port=5004, debug=True)
