from resources.microservice import MicroService
import config
import json
import requests
import logging

def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))

class Validate:
    @staticmethod
    def execute(request):
        response=MicroService.execute("GET",config.User_Server_Url+'/register',request.headers)
        if response.status_code>=400:
            return {'value':(response.json(),response.status_code),'pass':False}
        else:
            return {'value':response.json(),'pass':True}

    @staticmethod
    def admin(request):
        user_response=Validate.execute(request)
        if(not user_response['pass']):
            return {'pass':False,'value':user_response['value'] }
        if(not user_response['value']['is_admin']):
            return {'value':({'message':'Only admin is allowed to do this functionality'},401),'pass':False}

        return {'value':user_response['value'],'pass':True}

    @staticmethod
    def user(request):
        user_response=Validate.execute(request)
        if(not user_response['pass']):
            return {'pass':False,'value':user_response['value'] }
        return {'value':user_response['value'],'pass':True}

    @staticmethod
    def category(_id):
        try:      
            response = requests.request("GET",config.Product_Server_Url+'/category/{}'.format(_id))
        except Exception as e:
            error_msg_log(e)
            obj=MicroService()
            return {'value':(obj.json(),obj.status_code),'pass':False}
        if(response.status_code>=400):
            return {'value':(response.json(),response.status_code),'pass':False}
        else:
            return {'value':response.json(),'pass':True}

    @staticmethod
    def item(_id):
        try:      
            response = requests.request("GET",config.Product_Server_Url+'/item/{}'.format(_id))
        except Exception as e:
            error_msg_log(e)
            obj=MicroService()
            return {'value':(obj.json(),obj.status_code),'pass':False}
        if(response.status_code>=400):
            return {'value':(response.json(),response.status_code),'pass':False}
        else:
            return {'value':response.json(),'pass':True}

    

    
