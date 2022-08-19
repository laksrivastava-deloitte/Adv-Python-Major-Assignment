from urllib import response
from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate
import requests
import json
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))

class CartData(Resource):
    url=config.Cashflow_Server_Url+"/cartdata"

    #Category Single item Creation
    def post(self):
        try:
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
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class CartDataList(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}"

    #Get all items
    def get(self):
        try:
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']
            
            response=MicroService.execute("GET",CartDataList.url.format(user_response['value']['id']),request.headers)
            return response.json(),response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    #Delete all item
    def delete(self):
        try:
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']
            
            response=MicroService.execute("DELETE",CartDataList.url.format(user_response['value']['id']),request.headers)
            return response.json(),response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class CartSingleItem(Resource):
    url=config.Cashflow_Server_Url+"/cartdata/{}/{}"

    #Get Single Cart Item
    def get(self,product_id):
        try:
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']
            
            response=MicroService.execute("GET",CartSingleItem.url.format(user_response['value']['id'],product_id),request.headers)
            return response.json(),response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    #Delete Single Cart Item
    def delete(self,product_id):
        try:
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']
            
            response=MicroService.execute("DELETE",CartSingleItem.url.format(user_response['value']['id'],product_id),request.headers)
            return response.json(),response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input


class MakePayment(Resource):

    def post(self):
        try:
            #Check user is valid or not    user_response['value']['id]==>user_id
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']

            #List of all the added items in cart
            response=MicroService.execute_get(CartDataList.url.format(user_response['value']['id']))
            if(response.status_code>=400):
                return response.json(),response.status_code
            item_list=response.json()["cart items"]
            print(item_list)
            
            if(len(item_list)==0):
                return {"message":"Cart is empty"},400

            net_total=0
            prices_list=[]
            #validate items
            for itemjson in item_list:
                item_response=Validate.item(itemjson['product_id'])
                if(not item_response['pass']):
                    return item_response['value']
                prices_list.append(item_response['value']['item']['price'])
                net_total+= item_response['value']['item']['price']*itemjson['quantity']
                if(itemjson['quantity']>item_response['value']['item']['item_count']):
                    return {'message':f"{item_response['value']['item']['name']} has {item_response['value']['item']['item_count']} quantity only","advice":f"Please decrease the quantity from {itemjson['quantity']} to below max limit"},400

            response_payment=MicroService.execute_post(config.Cashflow_Server_Url+"/paymentdata",{"user_id": user_response['value']['id'], "net_total": net_total,**request.get_json()})
            if(response_payment.status_code>=400):
                return response_payment.json(),response_payment.status_code
            info=response_payment.json()['info']
            payment_id=response_payment.json()['data']['payment_id']


            i=-1
            #store item in paymentchild
            for itemjson in item_list:
                i+=1
                data={"item_id":itemjson['product_id'],"payment_id":payment_id,"price":prices_list[i],"quantity":itemjson['quantity'],"category_id":itemjson['category_id']}
                r1=MicroService.execute_post(config.Cashflow_Server_Url+"/paymentdatachild",data)
                if(r1.status_code>=400):
                    return r1.json(),r1.status_code
                #Reduce Item count
                r1=MicroService.execute_get(config.Product_Server_Url+"/decreaseItemCount/{}/{}".format(itemjson['product_id'],itemjson['quantity']))
                if(r1.status_code>=400):
                    return r1.json(),r1.status_code


            #clearing cart
            r1=MicroService.execute("DELETE",config.Cashflow_Server_Url+'/cartdata/{}'.format(user_response['value']['id']),request.headers,data)
            if(r1.status_code>=400):
                    return r1.json(),r1.status_code

            #single payment result
            single_payemnt_response=MicroService.execute("GET",config.Cashflow_Server_Url+'/singlepayment/{}'.format(payment_id),request.headers,data)
            if(single_payemnt_response.status_code>=400):
                    return single_payemnt_response.json(),single_payemnt_response.status_code


            result=single_payemnt_response.json()
            result['info']=info
            return result,single_payemnt_response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input


class PaymentListUser(Resource):

    def get(self):
        try:
            user_response=Validate.user(request)
            if(not user_response['pass']):
                return user_response['value']
            response=MicroService.execute("GET",config.Cashflow_Server_Url+'/paymentdata/{}'.format(user_response['value']['id']),request.headers)

            return response.json(),response.status_code
        except Exception as e:
            error_msg_log(e)
            return invalid_input







    