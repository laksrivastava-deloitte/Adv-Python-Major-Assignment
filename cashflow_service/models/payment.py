from db import db
from datetime import datetime
import pytz

class PaymentModel(db.Model):
    __tablename__='payment'

    payment_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    date_time=db.Column(db.DateTime)
    net_total=db.Column(db.Integer)
    amt_paid=db.Column(db.Integer)
    discount=db.Column(db.Float)
    promocode=db.Column(db.String(30))

    items=db.relationship('PaymentChildModel',lazy='dynamic')
    

    def __init__(self,user_id,net_total,discount=0,amt_paid=0,promocode=None):
        self.user_id=user_id
        self.net_total=net_total
        self.discount=discount
        self.amt_paid=amt_paid
        self.promocode=promocode
        self.date_time=datetime.now(pytz.timezone('Asia/Kolkata'))

    def json(self):
        return {'payment_id':self.payment_id,'user_id':self.user_id,'data_time':str(self.date_time.strftime("%d-%m-%Y %I:%M %p")),'amt_paid':self.amt_paid,'net_total':self.net_total,'discount':self.discount,'promocode':self.promocode}

    @classmethod
    def find_by_paymentid(cls,payment_id):
        return cls.query.filter_by(payment_id=payment_id).first()

    @classmethod
    def find_by_userid(cls,user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        