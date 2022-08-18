from flask_restful import Resource,request
from models.payment import PaymentModel

class PaymentData(Resource):
    #Category Single item Creation
    def get(self):
        data=request.get_json()

        #set discount,amt_paid,promocode based on net_total
        data['amt_paid']=data['net_total']

        payment = PaymentModel(**data)
        payment.save_to_db()
        return {'message':'Payment model created successfully','data':payment.json()},201   


class PaymentDataList(Resource):
    #Get all items
    def get(self,user_id):
        payments=PaymentModel.find_by_userid(user_id)
        if payments:
            result=[]
            for payment in payments:
                items=payment.items
                items=[item.json() for item in items]
                payment=payment.json()
                payment['items']=items
                result.append(payment)
            return {'payment items':result},200
        return {'message':'payment is empty'},200 

class SinglePayment(Resource):
    #Get single Payment
    def get(self,_id):
        payment=PaymentModel.find_by_paymentid(_id)
        items=payment.items
        items=[item.json() for item in items]
        payment=payment.json()
        payment['items']=items
        return {'data':payment},200
