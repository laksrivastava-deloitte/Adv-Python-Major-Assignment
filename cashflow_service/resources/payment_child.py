from flask_restful import Resource,request
from models.payment_child import PaymentChildModel

class PaymentDataChild(Resource):
    #Category Single item Creation
    def post(self):
        data=request.get_json()
        payment = PaymentChildModel(**data)
        payment.save_to_db()
        return {'message':'Payment model created successfully','data':payment.json()},201   
