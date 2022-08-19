from flask import Flask,request,jsonify, make_response, Response
from flask_restful import Api
from flask_jwt import JWT
import datetime
import time
from flask import g
from db import db
from resources.cart import CartData,CartDataList,CartSingleItem
from resources.payment import PaymentData,PaymentDataList,SinglePayment
from resources.payment_child import PaymentDataChild
from resources.promo import PromoData,PromoList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'    #database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Lakshya Srivastava Project'
api = Api(app)

#Run at start only
@app.before_first_request
def create_tables():
    db.create_all()

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

api.add_resource(CartData,'/cartdata')
api.add_resource(CartDataList,'/cartdata/<int:user_id>')
api.add_resource(CartSingleItem,'/cartdata/<int:user_id>/<int:product_id>')
api.add_resource(PaymentData,'/paymentdata')
api.add_resource(PaymentDataList,'/paymentdata/<int:user_id>')
api.add_resource(PaymentDataChild,'/paymentdatachild')
api.add_resource(SinglePayment,'/singlepayment/<int:_id>')
api.add_resource(PromoData,'/promodata/<string:name>')
api.add_resource(PromoList,'/promolist')




if __name__=='__main__':
    db.init_app(app)
    app.run(port=5003, debug=True)
