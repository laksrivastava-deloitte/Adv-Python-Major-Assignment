from flask_restful import Resource,request
import config
from resources.microservice import MicroService

class CartData(Resource):
    url=config.Cashflow_Server_Url+"/cartdata"

    #Category Single item Creation
    def post(self):
        response=MicroService.execute("POST",CartData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class CartDataList(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}"

    #Get all items
    def get(self,user_id):
        response=MicroService.execute("GET",CartDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

    #Delete all item
    def delete(self,user_id):
        response=MicroService.execute("DELETE",CartDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

class CartSingleItem(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}/{}"

    #Get Single Cart Item
    def get(self,user_id,product_id):
        response=MicroService.execute("GET",CartSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code

    #Delete Single Cart Item
    def delete(self,user_id,product_id):
        response=MicroService.execute("DELETE",CartSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code


class PaymentData(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata"

    #Category Single item Creation
    def post(self):
        response=MicroService.execute("POST",PaymentData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class PaymentDataList(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata/{}"

    #Get all items
    def get(self,user_id):
        response=MicroService.execute("GET",PaymentDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

    #Delete all item
    def delete(self,user_id):
        response=MicroService.execute("DELETE",PaymentDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

class PaymentSingleItem(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata/{}/{}"

    def get(self,user_id,product_id):
        response=MicroService.execute("GET",PaymentSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code

    def delete(self,user_id,product_id):
        response=MicroService.execute("DELETE",PaymentSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code






    