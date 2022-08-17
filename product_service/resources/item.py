from flask_restful import Resource,request
from models.item import ItemModel
# from models.category import CategoryModel

class ItemData(Resource):

    #Item Registration
    def post(self):
        data=request.get_json()

        if ItemModel.find_by_name(data['name']):
            return {"message":"A item with that name already exists"},400
        # print(data)
        item = ItemModel(**data)
        item.save_to_db()

        return {'message':'Item created successfully.','data':item.json()},201

    #Item Updation
    def put(self):
        data=request.get_json()
        item=ItemModel.find_by_name(data['name'])
        key_param=list(data.keys())
        if('price' in key_param):
            item.price=data['price']
        if('rating' in key_param):
            item.rating=data['rating']
        if('item_count' in key_param):
            item.item_count=data['item_count']
        item.save_to_db()
        return {'message':'Item updates successfully','data':item.json()},200

class SingleItem(Resource):

    #Item Deletion
    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_to_db()
            return {'message':'Item deleted successfully'},200
        return {'message':'Failed to delete,item not found'},400

    #Single Item detail
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return {'item':item.json()},200
        return {'message':'Item not found'},400
        

class ItemList(Resource):
    def post(self):
        try:
            data=request.get_json()
            inputparams=data.keys()
            # if('category' in inputparams):
            #     items=CategoryModel.find_by_name(data['category'])
            #     print(items)
            # else:
            items=[item.json() for item in ItemModel.query.all()]
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

class ReduceItemCount(Resource):
    def get(self,name,quantity):
        item=ItemModel.find_by_name(name)
        if (item and item.item_count>=quantity):
            item.item_count=item.item_count-quantity
            item.save_to_db()
            return {'item':item.json()},200
        elif item:
            return {'message':'Given quantity is greater than actual quantity,hence failed'},400
        else:
            return {'message':'Item not found'},400
