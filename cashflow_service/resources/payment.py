from flask_restful import Resource,request
from models.payment import PaymentModel
from models.promo import PromoModel

class PaymentData(Resource):
    #Category Single item Creation
    def post(self):
        data=request.get_json()
        info=""
        data['amt_paid']=data['net_total']
        # set discount,amt_paid,promocode based on net_total
        promoapplied=False
        if('promocode' in data.keys()):
            promo=PromoModel.find_by_name(data['promocode'])
            if(promo and data['net_total']>promo.min_amount):
                promoapplied=True
                data['discount']=promo.percentage*data['net_total']
                data['amt_paid']=data['net_total']-data['discount']
                info=f"Promocode {data['promocode']} successfully applied"
            else:
                info=f"Invalid Promocode {data['promocode']}"
                data['promocode']=None
                
        if(not promoapplied and 'promocode' not in data.keys()):
            max_amt=0
            discountpercent=0
            promolist=[promoitem for promoitem in PromoModel.query.all()]
            for promoitem in promolist:
                if(data['net_total']>promoitem.max_amount):
                    if(max_amt<promoitem.max_amount):
                        max_amt=promoitem.max_amount
                        discountpercent=promoitem.percentage
                        data['promocode']=promoitem.name
            if('promocode' in data.keys()):
                data['discount']=discountpercent*data['net_total']
                data['amt_paid']=data['net_total']-data['discount']
                info=f"Promocode {data['promocode']} automatically applied"

        payment = PaymentModel(**data)
        payment.save_to_db()
        return {'message':'Payment model created successfully','info':info,'data':payment.json()},201   


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
