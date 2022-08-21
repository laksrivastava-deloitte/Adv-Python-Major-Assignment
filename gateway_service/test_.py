import unittest
import requests
import json

url_gateway = "http://127.0.0.1:5004"
#Global object
header = {
    'Content-Type': 'application/json',
    'X-Access-Token': 'No Token'
}
test_user = {"username": "test_user", "password": "test_password", "is_admin": True}
test_category = ""
test_item = ""
test_promo=""
test_cartitem=""
test_payment=""

#String part of url
register = "/register"
promo_name="super10"
create_category="/createCategory"
login='/login'
newitem='/newItem'
category='/categ'+'ory/'
promodata='/promodata/'
cartdata='/cartdata'
item='/item/'

def execute(request_type, url, header=header, data={}):
    response = requests.request(
        request_type, url, headers=header, data=json.dumps(data))
    return response


class Test1_User(unittest.TestCase):

    def test_01_Registration_user(self):
        # first time registration
        response = execute("POST", url_gateway+register, header, test_user)
        self.assertEqual(response.status_code, 201)
        # Second time registration
        response = execute("POST", url_gateway+register, header, test_user)
        self.assertEqual(response.status_code, 406)

    def test_02_Login_user(self):
        global header
        response = execute("POST", url_gateway+login, header, test_user)
        self.assertEqual(response.status_code, 200)
        header['X-Access-Token']=response.json()['token']
        

    def test_03_Update_user(self):
        global header
        # update
        response = execute("PUT", url_gateway+register,
                           header, {'password': 'abcd'})
        self.assertEqual(response.status_code, 200)
        # relogin to get new token
        response = execute("POST", url_gateway+login, header,
                           {'username': test_user['username'], 'password': 'abcd'})
        self.assertEqual(response.status_code, 200)
        header['X-Access-Token']=response.json()['token']

    def test_04_Delete_user(self):
        response = execute("DELETE", url_gateway+register, header)
        self.assertEqual(response.status_code, 200)
        # delete again
        response = execute("DELETE", url_gateway+register, header)
        self.assertEqual(response.status_code, 401)


class Test2_Product(unittest.TestCase):

    def test_05_User_initiate(self):
        global header
        execute("POST", url_gateway+register, header, test_user)
        # self.assertEqual(response.status_code,201)
        response = execute("POST", url_gateway+login, header, test_user)
        self.assertEqual(response.status_code, 200)
        header['X-Access-Token']=response.json()['token']

    def test_06_Create_category(self):
        global test_category
        data = {"name": "Test Product"}
        # Create category
        response = execute("POST", url_gateway+create_category, header, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['data']['name'], data['name'])
        test_category = response.json()['data']
        # Recreate same category
        response = execute("POST", url_gateway+create_category, header, data)
        self.assertEqual(response.status_code, 406)

    def test_07_Create_item(self):
        global test_item
        global test_category
        data = {'name': 'Test Item', 'item_count': 100, "rating": 4,
                "price": 10, "category_id": test_category['id']}
        # Create item
        response = execute("POST", url_gateway+newitem, header, data)
        self.assertEqual(response.status_code, 201)
        test_item = response.json()['data']
        # Recreate same item
        response = execute("POST", url_gateway+newitem, header, data)
        self.assertEqual(response.status_code, 406)

    def test_08_Update_item(self):
        global test_category
        global test_item
        data = {'name': test_item['name'],
                "item_count": 700, "rating": 2, "price": 20}
        # Update item
        response = execute("PUT", url_gateway+newitem, header, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['price'], 20)
        self.assertEqual(response.json()['data']['rating'], 2)
        self.assertEqual(response.json()['data']['item_count'], 700)
        self.assertEqual(response.json()['data']
                         ['category_id'], test_category['id'])
        test_item = response.json()['data']

    def test_09_Get_category(self):
        global test_category
        global test_item
        response = execute("GET", url_gateway+category +
                           str(test_category['id']), header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['category']['name'], test_category['name'])
        self.assertEqual(
            response.json()['category']['id'], test_category['id'])
        self.assertDictEqual(
            response.json()['category']['items'][0], test_item)

    def test_10_All_category(self):
        global test_category
        global test_item
        response = execute("GET", url_gateway+'/categories', header)
        j=-1
        for i in response.json()['category']:
            j+=1
            if i['name']==test_category['name']:
                break
   
        self.assertEqual(response.json()['category'][j]['name'],test_category['name'])
        self.assertEqual(response.json()['category'][j]['id'],test_category['id'])
        self.assertDictEqual(response.json()['category'][j]['items'][0],test_item)

    def test_11_All_item_with_sortfilter(self):
        data={"sortBy":"price","sortDescending":True,"filterBy":"item_count","filterValue":7,"category":"Grocery"}
        response = execute("GET", url_gateway+'/categories', header,data)
        self.assertEqual(response.status_code,200)

    def test_12_get_item(self):
        global test_item
        response = execute("GET", url_gateway+item+str(test_item['id']), header)
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json()['item'],test_item)

    def test_13_Delete_item(self):
        global test_item
        # Delete item
        response = execute("DELETE", url_gateway+item +
                           test_item['name'], header)
        self.assertEqual(response.status_code, 200)
        # Redelete item
        response = execute("DELETE", url_gateway+item +
                           test_item['name'], header)
        self.assertEqual(response.status_code, 406)

    def test_14_Delete_category(self):
        global test_category
        # delete category
        response = execute("DELETE", url_gateway +
                           '/category/'+test_category['name'], header)
        self.assertEqual(response.status_code, 200)
      
        # redelete same category
        response = execute("DELETE", url_gateway +
                           '/category/'+test_category['name'], header)
        self.assertEqual(response.status_code, 406)
    

    def test_15_User_end(self):
        response = execute("DELETE", url_gateway+register, header)
        self.assertEqual(response.status_code, 200)

class Test3_CashFlow(unittest.TestCase):

    def test_16_User_category_item_initiate(self):
        global header
        global test_category
        global test_item

        #user create
        execute("POST", url_gateway+register, header, test_user)
        response = execute("POST", url_gateway+login, header, test_user)
        self.assertEqual(response.status_code, 200)
        header['X-Access-Token']=response.json()['token']

        # Create category
        data = {"name": "Test Product"}
        response = execute("POST", url_gateway+create_category, header, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['data']['name'], data['name'])
        test_category = response.json()['data']

        # Create item
        data = {'name': 'Test Item', 'item_count': 100, "rating": 4,"price": 10, "category_id": test_category['id']}
        response = execute("POST", url_gateway+newitem, header, data)
        self.assertEqual(response.status_code, 201)
        test_item = response.json()['data']


    def test_17_Create_promo(self):
        #create promo
        data={"min_amount":5,"max_amount":30,"percentage":0.02}
        response = execute("POST", url_gateway+promodata+promo_name, header, data)
        self.assertEqual(response.json()['result']['name'],promo_name)
        self.assertEqual(response.json()['result']['min_amount'],5)
        self.assertEqual(response.json()['result']['max_amount'],30)

        #recreate promo
        response = execute("POST", url_gateway+promodata+promo_name, header, data)
        self.assertEqual(response.status_code,406)

    def test_18_Update_promo(self):
        global test_promo
        data={"min_amount":10,"max_amount":40,"percentage":0.03}
        response = execute("PUT", url_gateway+promodata+promo_name, header, data)
        self.assertEqual(response.json()['result']['name'],promo_name)
        self.assertEqual(response.json()['result']['min_amount'],10)
        self.assertEqual(response.json()['result']['max_amount'],40)
        test_promo=response.json()['result']

    def test_19_All_promo(self):
        global test_promo
        response = execute("GET", url_gateway+'/promolist', header)
        j=-1
        for i in response.json()['promocodes']:
            j+=1
            if i['name']==promo_name:
                break
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json()['promocodes'][j],test_promo)


    def test_20_Insert_in_cart(self):
        global test_item
        global test_user
        global test_cartitem
        data={"product_id":test_item['id'],"quantity":5}
        response = execute("POST", url_gateway+cartdata, header,data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json()['data']['category_id'],test_item['category_id'])
        self.assertEqual(response.json()['data']['product_id'],test_item['id'])
        self.assertEqual(response.json()['data']['quantity'],5)
        test_cartitem=response.json()['data']

    def test_21_All_Cart_items(self):
        global test_cartitem
        response = execute("GET", url_gateway+cartdata, header)
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json()['cart items'][0],test_cartitem)

    def test_22_Get_single_cart_item(self):
        global test_item
        global test_cartitem
        response = execute("GET", url_gateway+'/cartdata/'+str(test_item['id']), header)
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json()['cart item'],test_cartitem)

    def test_23_Delete_single_cart_item(self):
        global test_item
        global test_cartitem
        #Delete single item
        response = execute("DELETE", url_gateway+'/cartdata/'+str(test_item['id']), header)
        self.assertEqual(response.status_code,200)
    
    def test_24_Delete_all_cart_item(self):
        #Insert item in cart
        data={"product_id":test_item['id'],"quantity":5}
        execute("POST", url_gateway+cartdata, header,data)

        #Delete all cart item
        response = execute("DELETE", url_gateway+cartdata, header)
        self.assertEqual(response.status_code,200)

        #Re-Delete all cart item
        response = execute("DELETE", url_gateway+cartdata, header)
        self.assertEqual(response.status_code,200)

    def test_25_Cart_checkout(self):
        global test_cartitem
        global test_item
        global test_payment

        #Insert item in cart
        data={"product_id":test_item['id'],"quantity":5}
        response=execute("POST", url_gateway+cartdata, header,data)
        test_cartitem=response.json()['data']

        #Cart Checkout
        response=execute("POST", url_gateway+'/makePayment', header,{"promocode":promo_name})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['data']['promocode'],promo_name)
        self.assertEqual(response.json()['data']['items'][0]['item_id'],test_item['id'])
        test_payment=response.json()['data']


    def test_26_Payment_history(self):
        global test_payment
        response=execute("GET", url_gateway+'/myPayments', header)
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json()['payment items'][len(response.json()['payment items'])-1],test_payment)

    def test_27_Delete_promo(self):
        #delete promo
        response = execute("Delete", url_gateway+promodata+promo_name, header)
        self.assertEqual(response.status_code,200)

        #re-delete promo
        response = execute("Delete", url_gateway+promodata+promo_name, header)
        self.assertEqual(response.status_code,406)

    def test_28_User_category_item_end(self):
        # delete category
        response = execute("DELETE", url_gateway +category+test_category['name'], header)
        self.assertEqual(response.status_code, 200)

        #user end
        response = execute("DELETE", url_gateway+register, header)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
