from flask_restful import Resource,request
from models.payment import PaymentModel

class PaymentData(Resource):
    #Category Single item Creation
    def post(self):
        data=request.get_json()

        if PaymentModel.find_by_userid_and_productid(data['user_id'],data['product_id']):
            return {"message":"Item already exists in payment"},400

        payment = PaymentModel(**data)
        payment.save_to_db()
        return {'message':'Item successfully added to payment','data':payment.json()},201   


class PaymentDataList(Resource):
    #Get all items
    def get(self,user_id):
        payments=PaymentModel.find_by_userid(user_id)
        if payments:
            result=[]
            for payment in payments:
                result.append(payment.json())
            return {'payment items':result},200
        return {'message':'payment is empty'},200       

    #Delete all item
    def delete(self,user_id):
        payment_list=PaymentModel.find_by_userid(user_id)
        for payment_item in payment_list:
            payment_item.delete_from_db()
        return {'message':'All payment item deleted successfully'},200

class PaymentSingleItem(Resource):
    def get(self,user_id,product_id):
        payment_item=PaymentModel.find_by_userid_and_productid(user_id,product_id)
        if(payment_item):
            return {'payment item':payment_item.json()}
        else:
            return{'message':'Item not found'},400

    def delete(self,user_id,product_id):
        payment_item=PaymentModel.find_by_userid_and_productid(user_id,product_id)
        if(payment_item):
            payment_item.delete_from_db()
        return {'message':'Item deleted successfully'}
