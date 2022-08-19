from flask_restful import Resource,request
from models.promo import PromoModel

class PromoData(Resource):
    #Category Single item Creation
    def post(self,name):
        data=request.get_json()
        if(PromoModel.find_by_name(name)):
            return {'message':"Promo with same name already exists"},400
        data['name']=name
        promo_item=PromoModel(**data)
        promo_item.save_to_db()
        return {'result':promo_item.json()},201

    def put(self,name):
        data=request.get_json()
        promo_item=PromoModel.find_by_name(name)
        if(not promo_item):
            return {'message':"Promo not found exists"},400
        if('min_amount' in data.keys()):
            promo_item.min_amount=data['min_amount']
        if('max_amount' in data.keys()):
            promo_item.max_amount=data['max_amount']
        if('percentage' in data.keys()):
            promo_item.percentage=data['percentage']

        promo_item.save_to_db()
        return {'result':promo_item.json()},200

    def delete(self,name):
        promo_item=PromoModel.find_by_name(name)
        if(promo_item):
            promo_item.delete_to_db()
            return {'message':'promo deleted successfully'},200
        return {'message':'promo not found'},400

class PromoList(Resource):
    #All promos
    def get(self):
        promo_jsons=[promo_item.json() for promo_item in PromoModel.query.all()]
        return {'promocodes':promo_jsons},200