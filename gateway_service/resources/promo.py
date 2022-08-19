from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate

class PromoData(Resource):
    url=config.Cashflow_Server_Url+"/promodata/"

    #Promo Creation
    def post(self,name):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("POST",PromoData.url+name,request.headers,request.get_json())
        return response.json(),response.status_code

    #Promo Updation
    def put(self,name):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("PUT",PromoData.url+name,request.headers,request.get_json())
        return response.json(),response.status_code

    #Promo Deletion
    def delete(self,name):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("DELETE",PromoData.url+name,request.headers)
        return response.json(),response.status_code

class PromoList(Resource):
    url=config.Cashflow_Server_Url+"/promolist"
    #All promos
    def get(self):
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
        
        response=MicroService.execute("GET",PromoList.url,request.headers)
        return response.json(),response.status_code