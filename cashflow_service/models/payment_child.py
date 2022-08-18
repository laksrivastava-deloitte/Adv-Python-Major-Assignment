from db import db
from sqlalchemy.sql import func

class PaymentChildModel(db.Model):
    __tablename__='payment_item'

    id=db.Column(db.Integer,primary_key=True)
    item_id=db.Column(db.Integer)
    payment_id=db.Column(db.Integer)
    quantity=db.Column(db.Integer)
    price=db.Column(db.Float)
    category_id=db.Column(db.Integer)

    payment_id=db.Column(db.Integer,db.ForeignKey('payment.payment_id'))
    category=db.relationship('PaymentModel')
    

    def __init__(self,item_id,payment_id,quantity,price,category_id):
        self.item_id=item_id
        self.payment_id=payment_id
        self.quantity=quantity
        self.quantity=quantity
        self.price=price
        self.category_id=category_id

    def json(self):
        return {'item_id':self.item_id,'payment_id':self.payment_id,'quantity':self.quantity,'price':self.price,'category_id':self.category_id}

    @classmethod
    def find_by_itemid_and_paymentid(cls,item_id,payment_id):
        return cls.query.filter_by(item_id=item_id,payment_id=payment_id).first()

    @classmethod
    def find_by_paymentid(cls,payment_id):
        return cls.query.filter_by(payment_id=payment_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        