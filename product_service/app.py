from flask import Flask,request,jsonify, make_response, Response
from flask_restful import Api
from flask_jwt import JWT
import datetime
import time
from flask import g
from db import db
from resources.category import CategoryData, CategoryList,SingleCategory
from resources.item import ItemData,ItemList,ReduceItemCount,SingleItem


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

api.add_resource(CategoryData,'/createCategory')
api.add_resource(SingleCategory,'/category/<string:name>')
api.add_resource(CategoryList,'/categories')
api.add_resource(ItemData,'/newItem')
api.add_resource(SingleItem,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(ReduceItemCount,'/decreaseItemCount/<int:_id>/<int:quantity>')



if __name__=='__main__':
    db.init_app(app)
    app.run(port=5002, debug=True)
