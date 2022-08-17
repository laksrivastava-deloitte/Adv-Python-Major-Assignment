from db import db
import jwt
from flask_restful import request
# from sqlalchemy.ext.mutable import MutableList
# from sqlalchemy import pickleType

class ItemModel(db.Model):

    __tablename__='items'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    item_count=db.Column(db.Integer)
    rating=db.Column(db.Integer)
    price=db.Column(db.Float)
    # total_person_rated=db.Column(db.String)
    # total_person_rated = db.Column(MutableList.as_mutable(pickleType),default=[])

    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('CategoryModel')

    # def __init__(self,name,item_count,rating,price,total_person_rated=""):
    def __init__(self,name,item_count,rating,price,category_id):
        self.name=name
        self.item_count=item_count
        self.rating=rating
        self.price=price
        self.category_id=category_id
        # self.total_person_rated=total_person_rated

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()


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
        return {'id':self.id,'name':self.name,'rating':self.rating,'price':self.price,'item_count':self.item_count,'category_id':self.category_id}

    # def get_total_person_rated(self):
    #     return self.total_person_rated

    # def set_total_person_rated(self,new_user_id):
    #     self.total_person_rated.append(new_user_id)


    def __str__(self):
        return f"id:{self.id}, name:{self.name}, rating:{self.rating}, price:{self.price}, item_count:{self.item_count}, category_id:{self.category_id}"
