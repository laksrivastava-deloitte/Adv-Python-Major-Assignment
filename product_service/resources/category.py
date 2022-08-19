from unicodedata import category
from flask_restful import Resource,request
from models.category import CategoryModel
from models.item import ItemModel
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))

class CategoryData(Resource):
    #Category Creation
    def post(self):
        try:
            data=request.get_json()

            if CategoryModel.find_by_name(data['name']):
                return {"message":"A category with that name already exists"},406
            # print(data)
            category = CategoryModel(**data)
            category.save_to_db()

            return {'message':'Category created successfully.','data':category.json()},201
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class SingleCategory(Resource):
    #Category Deletion
    def delete(self,name):
        try:
            category=CategoryModel.find_by_name(name)
            if category:
                for item in category.items:
                    item.delete_to_db()
                category.delete_from_db()
                return {'message':'category deleted successfully'},200
            return {'message':'Failed to delete,category not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    #Single category detail
    def get(self,name):
        try:
            _id=int(name)
            category=CategoryModel.find_by_id(_id)
            if category:
                return {'category':category.json()},200
            return {'message':'category not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input


class CategoryList(Resource):
    def get(self):
        try:
            return {'category':[category.json() for category in CategoryModel.query.all()]}
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    def post(self):
        try:
            data=request.get_json()
            inputparams=data.keys()
            if('category' in inputparams):
                category=CategoryModel.find_by_name(data['category'])
                items=category.json()['items']
            else:
                category=[category.json() for category in CategoryModel.query.all()]
                items=[]
                for single_category in category:
                    items.extend(single_category['items'])

            if set(inputparams).issubset({"filterBy","filterValue","sortBy","sortDescending",'category'}):

                if "filterBy" in inputparams:
                    if "filterValue" not in inputparams:
                        if data['filterBy']=="name":
                            data["filterValue"]="A"
                        else:
                            data["filterValue"]=0
                    items=[item for item in items if item[data['filterBy']]>=data["filterValue"]]

                if "sortBy" in inputparams:
                    if "sortDescending" not in inputparams:
                        data["sortDescending"]=False
                    items=sorted(items,key=lambda x:x[data['sortBy']],reverse=data['sortDescending'])

                return {'items':items},200
                
            elif len(data)==0:
                return {'items':items},200
            else:
                return {'message':'Invalid body input'},400
        except Exception as e:
            error_msg_log(e)
            return invalid_input


    
        