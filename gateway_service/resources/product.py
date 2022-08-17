from flask_restful import Resource,request
import config
from resources.microservice import MicroService

class CategoryData(Resource):
    url=config.Product_Server_Url+"/createCategory"

    #Category Creation
    def post(self):
        response=MicroService.execute("POST",CategoryData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class SingleCategory(Resource):
    url=config.Product_Server_Url+"/category/{}"

    #Category Deletion
    def delete(self,name):
        response=MicroService.execute("DELETE",SingleCategory.url.format(name),request.headers)
        return response.json(),response.status_code

    #Single category detail
    def get(self,name):
        response=MicroService.execute("GET",SingleCategory.url.format(name),request.headers)
        return response.json(),response.status_code

class CategoryList(Resource):
    url=config.Product_Server_Url+"/categories"

    #List of all category
    def get(self):
        response=MicroService.execute("GET",CategoryList.url,request.headers)
        return response.json(),response.status_code

    #List of category with filter and sort functionality
    def post(self):
        response=MicroService.execute("POST",CategoryList.url,request.headers,request.get_json())
        return response.json(),response.status_code

class ItemData(Resource):
    url=config.Product_Server_Url+"/newItem"

    #Item Registration
    def post(self):
        response=MicroService.execute("POST",ItemData.url,request.headers,request.get_json())
        return response.json(),response.status_code

    #Item Updation
    def put(self):
        response=MicroService.execute("PUT",ItemData.url,request.headers,request.get_json())
        return response.json(),response.status_code

class SingleItem(Resource):
    url=config.Product_Server_Url+"/item/{}"

    #Item Deletion
    def delete(self,name):
        response=MicroService.execute("DELETE",SingleItem.url.format(name),request.headers)
        return response.json(),response.status_code
        
    #Single Item detail
    def get(self,name):
        response=MicroService.execute("GET",SingleItem.url.format(name),request.headers)
        return response.json(),response.status_code

class ItemList(Resource):
    url=config.Product_Server_Url+"/items"

    #All Items
    def post(self):
        response=MicroService.execute("POST",ItemList.url,request.headers,request.get_json())
        return response.json(),response.status_code

class ReduceItemCount(Resource):
    url=config.Product_Server_Url+"/decreaseItemCount/{}/{}"

    #Reduce item_count of response item
    def get(self,name,quantity):
        response=MicroService.execute("GET",SingleCategory.url.format(name,quantity),request.headers)
        return response.json(),response.status_code


