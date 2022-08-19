from flask import Flask
from flask_restful import Api
import time
from flask import g
# from resources.cashflow 
from resources.user import  UserData,UserList,UserLogin
from resources.product import CategoryData,CategoryList,SingleCategory,ItemData,SingleItem,ItemList,ReduceItemCount
from resources.cashflow import CartData,CartDataList,CartSingleItem,MakePayment,PaymentListUser
from resources.promo import PromoData,PromoList
# from resource.product


app = Flask(__name__)
app.secret_key = 'Lakshya Srivastava Project'
api = Api(app)

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
