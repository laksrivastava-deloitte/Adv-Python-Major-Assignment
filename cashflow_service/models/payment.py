from db import db

class PaymentModel(db.Model):
    __tablename__='payment'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer)
    data_time=db.Column(db.DateTime)
    quantity=db.Column(db.Integer)
    amt_paid=db.Column(db.Integer)
    net_total=db.Column(db.Integer)
    discount=db.Column(db.Integer)
    promocode=db.Column(db.String(30))
    

    def __init__(self,user_id,product_id,category_id,quantity,amt_paid,net_total,discount,promocode=None):
        self.user_id=user_id
        self.product_id=product_id
        self.category_id=category_id
        self.quantity=quantity
        self.amt_paid=amt_paid
        self.user_id=user_id
        self.user_id=user_id
        self.user_id=user_id

    def json(self):
        return {'id':self.id,'user_id':self.user_id,'category_id':self.category_id,'product_id':self.product_id,'quantity':self.quantity,'amt_paid':self.amt_paid,'net_total':self.net_total,'discount':self.discount,'promocode':self.promocode}

    @classmethod
    def find_by_userid(cls,user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        