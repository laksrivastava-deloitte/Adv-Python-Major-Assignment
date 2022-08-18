from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate

class CartData(Resource):
    url=config.Cashflow_Server_Url+"/cartdata"

    #Category Single item Creation
    def post(self):

        data=request.get_json()

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        item_response=Validate.item(data['product_id'])
        if(not item_response['pass']):
            return item_response['value']
        
        data['user_id']=user_response['value']['id']
        data['category_id']=item_response['value']['item']['category_id']

        response=MicroService.execute("POST",CartData.url,request.headers,data)
        return response.json(),response.status_code

class CartDataList(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}"

    #Get all items
    def get(self):
        
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("GET",CartDataList.url.format(user_response['value']['id']),request.headers)
        return response.json(),response.status_code

    #Delete all item
    def delete(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("DELETE",CartDataList.url.format(user_response['value']['id']),request.headers)
        return response.json(),response.status_code

class CartSingleItem(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}/{}"

    #Get Single Cart Item
    def get(self,product_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("GET",CartSingleItem.url.format(user_response['value']['id'],product_id),request.headers)
        return response.json(),response.status_code

    #Delete Single Cart Item
    def delete(self,product_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("DELETE",CartSingleItem.url.format(user_response['value']['id'],product_id),request.headers)
        return response.json(),response.status_code


class PaymentData(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata"

    #Category Single item Creation
    def post(self):
        data=request.get_json()
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("GET",CartDataList.url.format(user_response['value']['id']),request.headers)
        item_list=response.json()["cart items"]
        
        if(len(item_list)==0):
            return {"message":"Cart is empty"},400

        net_total=0

        for itemjson in item_list:
            item_response=Validate.item(request.get_json()['category_id'])
            if(not item_response['pass']):
                return item_response['value']
            net_total+= item_response['value']['price']
            if(itemjson['quantity']>item_response['value']['price']):
                return {'message':f"{item_response['value']['name']} has {item_response['value']['price']} quantity only","advice":"Please decrease the quantity below max limit"},400
        data['net_total']=net_total
            

        ####################################
        
         
        response=MicroService.execute("POST",PaymentData.url,request.headers,data)
        return response.json(),response.status_code

class PaymentDataList(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata/{}"

    #Get all items
    def get(self,user_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("GET",PaymentDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

    #Delete all item
    def delete(self,user_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("DELETE",PaymentDataList.url.format(user_id),request.headers)
        return response.json(),response.status_code

class PaymentSingleItem(Resource):
    url=config.Cashflow_Server_Url+"/paymentdata/{}/{}"

    def get(self,user_id,product_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("GET",PaymentSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code

    def delete(self,user_id,product_id):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
         
        response=MicroService.execute("DELETE",PaymentSingleItem.url.format(user_id,product_id),request.headers)
        return response.json(),response.status_code






    