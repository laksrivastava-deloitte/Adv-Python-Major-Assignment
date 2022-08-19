from db import db

class PromoModel(db.Model):

    __tablename__='promo'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    min_amount=db.Column(db.Integer)
    max_amount=db.Column(db.Integer)
    percentage=db.Column(db.Float)
    
    
    def __init__(self,name,min_amount,max_amount,percentage):
        self.name=name
        self.min_amount=min_amount
        self.max_amount=max_amount
        self.percentage=percentage

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id':self.id,'name':self.name,'min_amount':self.min_amount,'max_amount':self.max_amount,'percentage':self.percentage}

