from unicodedata import category
from flask_restful import Resource,request
from models.category import CategoryModel
from models.item import ItemModel

class CategoryData(Resource):
    #Category Creation
    def post(self):
        data=request.get_json()

        if CategoryModel.find_by_name(data['name']):
            return {"message":"A category with that name already exists"},400
        # print(data)
        category = CategoryModel(**data)
        category.save_to_db()

        return {'message':'Category created successfully.','data':category.json()},201

class SingleCategory(Resource):
    #Category Deletion
    def delete(self,name):
        category=CategoryModel.find_by_name(name)
        if category:
            for item in category.items:
                item.delete_to_db()
            category.delete_from_db()
            return {'message':'category deleted successfully'},200
        return {'message':'Failed to delete,category not found'},400

    #Single category detail
    def get(self,name):
        category=CategoryModel.find_by_name(name)
        if category:
            return {'category':category.json()},200
        return {'message':'category not found'},400


class CategoryList(Resource):
    def get(self):
        return {'category':[category.json() for category in CategoryModel.query.all()]}

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
        except:
            return {'message':'Invalid key value pair in body'},400


    
        