from flask_restful import Resource,request
from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt

class UserData(Resource):

    #User Registration
    def post(self):
        data=request.get_json()
        data['password']=generate_password_hash(data['password'], method='sha256')

        if UserModel.find_by_username(data['username']):
            return {"message":"A user with that username already exists"},400
        # print(data)
        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User created successfully.'},201

    #Registered User password Updation
    def put(self):
        #token Validation
        token_result=UserModel.validate_token()
        if(not token_result['pass']):
            return token_result['msg']

        data=request.get_json()
        token_result['value'].password=generate_password_hash(data['password'], method='sha256')
        token_result['value'].save_to_db()
        return {'message':'Password updated successfully'},200

    #Registered User delete
    def delete(self):
        #token Validation
        token_result=UserModel.validate_token()
        if(not token_result['pass']):
            return token_result['msg']

        token_result['value'].delete_to_db()
        return {'message':'User deleted successfully'}

    #Get User
    def get(self):
        token_result=UserModel.validate_token()
        if(not token_result['pass']):
            return token_result['msg']
        # print(token_result)
        return token_result['value'].json(),200


class UserLogin(Resource):
    #User Login
    def post(self):
        data=request.get_json()
        user=UserModel.find_by_username(data['username'])

        if not user:
            return {'message':'Invalid credentials'},400

        if check_password_hash(user.password, data['password']):
            SECRET_KEY = 'Lakshya Srivastava Project'
            token = jwt.encode({'name' : user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, SECRET_KEY)

            response = {'token' : token.decode('UTF-8')}
            return response

        return {"message":"Invalid Credentials"},400

class UserList(Resource):
    #All Registered Users list
    def get(self):
        #token Validation
        token_result=UserModel.validate_token()
        if(not token_result['pass']):
            return token_result['msg']
        print(token_result)
        if(token_result['value'].is_admin):
            return {'users':[user.json() for user in UserModel.query.all()]},200
        return {'message':'Only admin are allowed to use this functionality'},400

        