from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate

class UserData(Resource):
    url=config.User_Server_Url+"/register"

    #User Registration
    def post(self):
        response=MicroService.execute("POST",UserData.url,request.headers,request.get_json())
        return response.json(),response.status_code

    #Registered User password Updation
    def put(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("PUT",UserData.url,request.headers,request.get_json())
        return response.json(),response.status_code
    
    #Registered User delete
    def delete(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("DELETE",UserData.url,request.headers)
        return response.json(),response.status_code

class UserLogin(Resource):
    url=config.User_Server_Url+"/login"

    #User Login
    def post(self):
        response=MicroService.execute("POST",UserLogin.url,request.headers,request.get_json())
        return response.json(),response.status_code

class UserList(Resource):
    url=config.User_Server_Url+"/users"

    #All Registered Users list
    def get(self):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']
            
        response=MicroService.execute("GET",UserList.url,request.headers)
        return response.json(),response.status_code


