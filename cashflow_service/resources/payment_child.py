from flask_restful import Resource,request
from models.payment_child import PaymentChildModel
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))


class PaymentDataChild(Resource):
    #Category Single item Creation
    def post(self):
        try:
            data=request.get_json()
            payment = PaymentChildModel(**data)
            payment.save_to_db()
            return {'message':'Payment model created successfully','data':payment.json()},201   
        except Exception as e:
            error_msg_log(e)
            return invalid_input
