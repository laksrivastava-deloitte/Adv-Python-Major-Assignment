from flask import Flask,request,jsonify, make_response, Response
from flask_restful import Api
from flask_jwt import JWT
import datetime
import time
from flask import g
from db import db


from resources.user import UserData,UserLogin,UserList


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

api.add_resource(UserData,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(UserList,'/users')

if __name__=='__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
