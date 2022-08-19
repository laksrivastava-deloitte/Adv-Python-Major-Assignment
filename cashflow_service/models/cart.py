from db import db
from datetime import datetime
import pytz


class CartModel(db.Model):

    __tablename__='cart'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer)
    date_time=db.Column(db.DateTime)
    quantity=db.Column(db.Integer)
    
    
    def __init__(self,user_id,product_id,category_id,quantity):
        self.user_id=user_id
        self.product_id=product_id
        self.category_id=category_id
        self.quantity=quantity
        self.date_time=datetime.now(pytz.timezone('Asia/Kolkata'))

    @classmethod
    def find_by_userid_and_productid(cls,userid,productid):
        return cls.query.filter_by(user_id=userid,product_id=productid).first()

    @classmethod
    def find_by_userid(cls,userid):
        return cls.query.filter_by(user_id=userid)


    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id':self.id,'user_id':self.user_id,'product_id':self.product_id,'category_id':self.category_id,'date_time':str(self.date_time.strftime("%d-%m-%Y %I:%M %p")),'quantity':self.quantity}

