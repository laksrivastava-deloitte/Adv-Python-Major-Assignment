from flask_restful import Resource,request
from models.item import ItemModel
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))


class ItemData(Resource):

    #Item Registration
    def post(self):
        try:
            data=request.get_json()

            if ItemModel.find_by_name(data['name']):
                return {"message":"A item with that name already exists"},406
            # print(data)
            item = ItemModel(**data)
            item.save_to_db()

            return {'message':'Item created successfully.','data':item.json()},201
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    #Item Updation
    def put(self):
        try:
            data=request.get_json()
            item=ItemModel.find_by_name(data['name'])
            if item:
                key_param=list(data.keys())
                if('price' in key_param):
                    item.price=data['price']
                if('rating' in key_param):
                    item.rating=data['rating']
                if('item_count' in key_param):
                    item.item_count=data['item_count']
                item.save_to_db()
                return {'message':'Item updates successfully','data':item.json()},200
            else:
                return {'message':'No Item found to update'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class SingleItem(Resource):

    #Item Deletion
    def delete(self,name):
        try:
            item=ItemModel.find_by_name(name)
            if item:
                item.delete_to_db()
                return {'message':'Item deleted successfully'},200
            return {'message':'Failed to delete,item not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    #Single Item detail
    def get(self,name):
        try:
            _id=int(name)
            item=ItemModel.find_by_id(_id)
            if item:
                return {'item':item.json()},200
            return {'message':'Item not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input
        

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
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class ReduceItemCount(Resource):
    def get(self,_id,quantity):
        try:
            item=ItemModel.find_by_id(_id)
            if (item and item.item_count>=quantity):
                item.item_count=item.item_count-quantity
                item.save_to_db()
                return {'item':item.json()},200
            elif item:
                return {'message':'Given quantity is greater than actual quantity,hence failed'},406
            else:
                return {'message':'Item not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input
