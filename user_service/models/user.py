from db import db
import jwt
from flask_restful import request

class UserModel(db.Model):

    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80))
    password=db.Column(db.String(80))
    is_admin=db.Column(db.Boolean,default=False)

    def __init__(self,username,password,is_admin=False):
        #here sqlalchemy will give us id
        self.username=username
        self.password=password
        self.is_admin=is_admin

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()


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
        return {'username':self.username,'password':self.password,'is_admin':self.is_admin,'id':self.id}

    def __str__(self):
        return f"username:{self.username}, password:{self.password}, is_admin:{self.is_admin}"

    
    @staticmethod
    def validate_token():
        token = None
        result={'pass':False}
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            result['msg']= {'message' : 'Token is missing!'}, 401
            return result


        
        SECRET_KEY = 'Lakshya Srivastava Project'
        try:
            data = jwt.decode(token,SECRET_KEY)
            current_user = UserModel.find_by_username(data['name'])
        except Exception:
            result['msg']={'message' : 'Token is invalid!'}, 401
            return result

        if(current_user is None):
            result['msg']={'message' : 'Token is invalid!'}, 401
            return result
            
        result['pass']=True
        result['value']=current_user
        return result