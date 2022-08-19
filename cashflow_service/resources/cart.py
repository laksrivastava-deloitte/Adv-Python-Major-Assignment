from flask_restful import Resource,request
from models.cart import CartModel
import logging

invalid_input={'message':"Invalid input"},400
def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))

class CartData(Resource):
    #Category Single item Creation
    def post(self):
        try:
            data=request.get_json()

            if CartModel.find_by_userid_and_productid(data['user_id'],data['product_id']):
                return {"message":"Item already exists in cart"},406

            cart = CartModel(**data)
            cart.save_to_db()
            return {'message':'Item successfully added to cart','data':cart.json()},201
        except Exception as e:
            error_msg_log(e)
            return invalid_input  


class CartDataList(Resource):
    #Get all items
    def get(self,user_id):
        try:
            carts=CartModel.find_by_userid(user_id)
            if carts:
                result=[]
                for cart in carts:
                    result.append(cart.json())
                return {'cart items':result},200
            return {'message':'Cart is empty'},200
        except Exception as e:
            error_msg_log(e)
            return invalid_input       

    #Delete all item
    def delete(self,user_id):
        try:
            cartList=CartModel.find_by_userid(user_id)
            for cart_item in cartList:
                cart_item.delete_to_db()
            return {'message':'All cart item deleted successfully'},200
        except Exception as e:
            error_msg_log(e)
            return invalid_input

class CartSingleItem(Resource):
    def get(self,user_id,product_id):
        try:
            cart_item=CartModel.find_by_userid_and_productid(user_id,product_id)
            if(cart_item):
                return {'cart item':cart_item.json()}
            else:
                return{'message':'Item not found'},406
        except Exception as e:
            error_msg_log(e)
            return invalid_input

    def delete(self,user_id,product_id):
        try:
            cart_item=CartModel.find_by_userid_and_productid(user_id,product_id)
            if(cart_item):
                cart_item.delete_to_db()
            return {'message':'Item deleted successfully'}
        except Exception as e:
            error_msg_log(e)
            return invalid_input

        


