from email import message
from flask_restful import Resource,request
import config
from resources.microservice import MicroService
from resources.validate import Validate

class CategoryData(Resource):
    url=config.Product_Server_Url+"/createCategory"

    #Category Creation
    def post(self):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("POST",CategoryData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class SingleCategory(Resource):
    url=config.Product_Server_Url+"/category/{}"

    #Category Deletion
    def delete(self,name):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("DELETE",SingleCategory.url.format(name),request.headers)
        return response.json(),response.status_code

    #Single category detail
    def get(self,name):
        
        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        category_response=Validate.category(name)
        if(not category_response['pass']):
            return category_response['value']
        return category_response['value'],200
        

class CategoryList(Resource):
    url=config.Product_Server_Url+"/categories"

    #List of all category
    def get(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("GET",CategoryList.url,request.headers)
        return response.json(),response.status_code

    #List of category with filter and sort functionality
    def post(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("POST",CategoryList.url,request.headers,request.get_json())
        return response.json(),response.status_code

class ItemData(Resource):
    url=config.Product_Server_Url+"/newItem"

    #Item Registration
    def post(self):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        category_response=Validate.category(request.get_json()['category_id'])
        if(not category_response['pass']):
            return category_response['value']

        response=MicroService.execute("POST",ItemData.url,request.headers,request.get_json())
        return response.json(),response.status_code

    #Item Updation
    def put(self):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("PUT",ItemData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class SingleItem(Resource):
    url=config.Product_Server_Url+"/item/{}"

    #Item Deletion
    def delete(self,name):

        user_response=Validate.admin(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("DELETE",SingleItem.url.format(name),request.headers)
        return response.json(),response.status_code
        
    #Single Item detail
    def get(self,name):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        item_response=Validate.item(name)
        if(not item_response['pass']):
            return item_response['value']
        return item_response['value'],200

class ItemList(Resource):
    url=config.Product_Server_Url+"/items"

    #All Items
    def post(self):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("POST",ItemList.url,request.headers,request.get_json())
        return response.json(),response.status_code

class ReduceItemCount(Resource):
    url=config.Product_Server_Url+"/decreaseItemCount/{}/{}"

    #Reduce item_count of response item
    def get(self,name,quantity):

        user_response=Validate.user(request)
        if(not user_response['pass']):
            return user_response['value']

        response=MicroService.execute("GET",ReduceItemCount.url.format(name,quantity),request.headers)
        return response.json(),response.status_code


