from flask_restful import Resource,request
from models.cart import CartModel

class CartData(Resource):
    #Category Single item Creation
    def post(self):
        data=request.get_json()

        if CartModel.find_by_userid_and_productid(data['user_id'],data['product_id']):
            return {"message":"Item already exists in cart"},400

        cart = CartModel(**data)
        cart.save_to_db()
        return {'message':'Item successfully added to cart','data':cart.json()},201  


class CartDataList(Resource):
    #Get all items
    def get(self,user_id):
        carts=CartModel.find_by_userid(user_id)
        if carts:
            result=[]
            for cart in carts:
                result.append(cart.json())
            return {'cart items':result},200
        return {'message':'Cart is empty'},200       

    #Delete all item
    def delete(self,user_id):
        cartList=CartModel.find_by_userid(user_id)
        for cart_item in cartList:
            cart_item.delete_to_db()
        return {'message':'All cart item deleted successfully'},200

class CartSingleItem(Resource):
    def get(self,user_id,product_id):
        cart_item=CartModel.find_by_userid_and_productid(user_id,product_id)
        if(cart_item):
            return {'cart item':cart_item.json()}
        else:
            return{'message':'Item not found'},400

    def delete(self,user_id,product_id):
        cart_item=CartModel.find_by_userid_and_productid(user_id,product_id)
        if(cart_item):
            cart_item.delete_to_db()
        return {'message':'Item deleted successfully'}

        


