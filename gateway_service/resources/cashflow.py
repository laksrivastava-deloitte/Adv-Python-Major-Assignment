from urllib import response
from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate
import requests
import json

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


class MakePayment(Resource):

    def get(self):
        #Check user is valid or not    user_response['value']['id]==>user_id
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        #List of all the added items in cart
        response=MicroService.execute("GET",CartDataList.url.format(user_response['value']['id']),request.headers)
        item_list=response.json()["cart items"]
        print(item_list)
        
        if(len(item_list)==0):
            return {"message":"Cart is empty"},400

        net_total=0
        pricesList=[]
        #validate items
        for itemjson in item_list:
            item_response=Validate.item(itemjson['product_id'])
            if(not item_response['pass']):
                return item_response['value']
            pricesList.append(item_response['value']['item']['price'])
            net_total+= item_response['value']['item']['price']*itemjson['quantity']
            if(itemjson['quantity']>item_response['value']['item']['item_count']):
                return {'message':f"{item_response['value']['item']['name']} has {item_response['value']['item']['item_count']} quantity only","advice":f"Please decrease the quantity from {itemjson['quantity']} to below max limit"},400

        #create payment       gives payment_id
        headers = {'Content-Type': 'application/json'}
        response_payment = requests.request("GET", config.Cashflow_Server_Url+"/paymentdata", headers=headers, data=json.dumps({"user_id": user_response['value']['id'], "net_total": net_total}))
        payment_id=response_payment.json()['data']['payment_id']


        i=-1
        #store item in paymentchild
        for itemjson in item_list:
            i+=1
            data={"item_id":itemjson['product_id'],"payment_id":payment_id,"price":pricesList[i],"quantity":itemjson['quantity'],"category_id":itemjson['category_id']}
            requests.request("POST", config.Cashflow_Server_Url+"/paymentdatachild", headers=headers, data=json.dumps(data))
            #Reduce Item count
            requests.request("GET", config.Product_Server_Url+"/decreaseItemCount/{}/{}".format(itemjson['product_id'],itemjson['quantity']), headers=headers,data="")


        #clearing cart
        MicroService.execute("DELETE",config.Cashflow_Server_Url+'/cartdata/{}'.format(user_response['value']['id']),request.headers,data)

        #single payment result
        single_payemnt_response=MicroService.execute("GET",config.Cashflow_Server_Url+'/singlepayment/{}'.format(payment_id),request.headers,data)

        return single_payemnt_response.json(),single_payemnt_response.status_code


class PaymentListUser(Resource):

    def get(self):
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']
        response=MicroService.execute("GET",config.Cashflow_Server_Url+'/paymentdata/{}'.format(user_response['value']['id']),request.headers)

        return response.json(),response.status_code

class AllPayments(Resource):
    def get(self):
        pass






    