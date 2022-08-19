from flask_restful import Resource,request
from models.promo import PromoModel
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))


class PromoData(Resource):
    #Category Single item Creation
    def post(self,name):
        try:
            data=request.get_json()
            if(PromoModel.find_by_name(name)):
                return {'message':"Promo with same name already exists"},406
            data['name']=name
            promo_item=PromoModel(**data)
            promo_item.save_to_db()
            return {'result':promo_item.json()},201
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    def put(self,name):
        try:
            data=request.get_json()
            promo_item=PromoModel.find_by_name(name)
            if(not promo_item):
                return {'message':"Promo not found exists"},406
            if('min_amount' in data.keys()):
                promo_item.min_amount=data['min_amount']
            if('max_amount' in data.keys()):
                promo_item.max_amount=data['max_amount']
            if('percentage' in data.keys()):
                promo_item.percentage=data['percentage']

            promo_item.save_to_db()
            return {'result':promo_item.json()},200
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    def delete(self,name):
        try:
            promo_item=PromoModel.find_by_name(name)
            if(promo_item):
                promo_item.delete_to_db()
                return {'message':'promo deleted successfully'},200
            return {'message':'promo not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input
        

class PromoList(Resource):
    #All promos
    def get(self):
        try:
            promo_jsons=[promo_item.json() for promo_item in PromoModel.query.all()]
            return {'promocodes':promo_jsons},200
        except Exception as e:
            error_msg_log(e)
            return invalid_input