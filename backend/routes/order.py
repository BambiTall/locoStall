from flask import Blueprint, Flask, request, jsonify, make_response, redirect
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import json
from sqlalchemy.sql import func
from ..extentions import db
from ..models.user import User
from ..models.orders import Orders
from ..models.menu import Menu
from ..models.shop_name import Shop_name
#sandy
import time
import json
import requests
import hashlib
import hmac
import base64
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

load_dotenv()
#sandy

order_bp = Blueprint('order_bp', __name__)


# Get order list
@order_bp.route(f'{os.environ["API_BASE"]}/orders')
def get_orders_list():
    orders = db.session.execute(db.select(Orders).order_by(Orders.id)).scalars()

    return [order.json() for order in orders]


# Get user orders
@order_bp.route(f'{os.environ["API_BASE"]}/orders/user/<int:user_id>')
def get_user_order_list(user_id):
    user = User.query.filter_by(id=user_id).first()
    orders = (
        Orders.query.filter_by(user_id=user_id).order_by(Orders.updated_at.desc()).all()
    )
    order_list = [order.json() for order in orders]

    for order in order_list:
        shop = Shop_name.query.filter_by(
            shop_id=order["shop_id"], lang=user.native_lang
        ).first()
        order["shop_name"] = shop.name
        item_list = json.loads(order["item_list"])
        new_item_list = []
        for item in item_list:
            menu = Menu.query.filter_by(
                shop_id=order["shop_id"],
                prod_id=item["prod_id"],
                lang=user.native_lang,
            ).first()
            item["name"] = menu.name
            item["price"] = menu.price
            new_item_list.append(item)
        order["item_list"] = json.dumps(new_item_list)

    return jsonify(order_list)


# Get shop orders by manager's user id
@order_bp.route(f'{os.environ["API_BASE"]}/orders/manager/<int:user_id>')
def get_manager_order_list(user_id):
    user = User.query.filter_by(id=user_id).first()
    orders = (
        Orders.query.filter_by(shop_id=user.shop_id)
        .order_by(Orders.created_at.desc())
        .all()
    )
    order_list = [order.json() for order in orders]

    for order in order_list:
        item_list = json.loads(order["item_list"])
        new_item_list = []
        for item in item_list:
            menu = Menu.query.filter_by(
                shop_id=order["shop_id"],
                prod_id=item["prod_id"],
                lang=user.native_lang,
            ).first()
            item["name"] = menu.name
            item["price"] = menu.price
            new_item_list.append(item)
        order["item_list"] = json.dumps(new_item_list)

    return jsonify(order_list)


# Get order detail
@order_bp.route(
    f'{os.environ["API_BASE"]}/<lang>/order_detail/<int:order_id>', methods=['GET']
)
def get_orders_detail(lang, order_id):
    order = db.get_or_404(Orders, order_id).json()
    shop = Shop_name.query.filter_by(shop_id=order["shop_id"], lang=lang).first()
    order["shop_name"] = shop.name
    item_list = json.loads(order["item_list"])
    new_item_list = []
    for item in item_list:
        menu = Menu.query.filter_by(
            shop_id=order["shop_id"],
            prod_id=item["prod_id"],
            lang=lang,
        ).first()
        item["name"] = menu.name
        item["price"] = menu.price
        new_item_list.append(item)
    order["item_list"] = json.dumps(new_item_list)

    return {"data": order}


# Add order
@order_bp.route(f'{os.environ["API_BASE"]}/send_order', methods=['POST'])
def add_order():
    data = request.get_json()

    item_list_json = json.dumps(data['item_list'])

    orders = Orders(
        item_list=item_list_json,
        user_id=data['user_id'],
        payment=data['payment'],
        shop_id=data['shop_id'],
        state="waiting",
    )

    db.session.add(orders)
    db.session.commit()

    return {"message": "送出訂單成功", "data": orders.json()}


# Update order (require datas : order's id, state)
@order_bp.route(f'{os.environ["API_BASE"]}/update_order', methods=['POST'])
def update_order():
    data = request.get_json()
    order = db.get_or_404(entity=Orders, ident=data['order_id'])
    order.state = data['state']
    # order.waiting = data['waiting']
    db.session.commit()

    return {'message': 'Order state updated successfully'}, 200


    con_url = f"/v3/payments/{transaction_id}/confirm"
    conf_data = json.dumps({
                "amount": amount,
                "currency": currency
                })
    headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, con_url, conf_data, nonce)
    response = requests.post("https://sandbox-api-pay.line.me"+con_url, headers=headers, data=conf_data)
    print(response.text)
    response = json.loads(response.text)

    return response.get('returnMessage')

#sandy-linepay_呼叫付款
@order_bp.route(f'{os.environ["API_BASE"]}/linepay', methods=['GET']) #send-order=linepay
def linepay_order():
    # data = request.get_json()

    # item_list_json = json.dumps(data['item_list'])

    # orders = Orders(
    #     item_list=item_list_json,
    #     user_id=data['user_id'],
    #     payment=data['payment'],
    #     shop_id=data['shop_id'],
    #     state="waiting",
    # )

    # db.session.add(orders)
    # db.session.commit()

    #sandy-linepay_定義付款
    channel_id = os.environ.get("LINEPAY_CHANNEL_ID")
    channel_secret = os.environ.get("LINEPAY_CHANNEL_SECRET_KEY")

    headers = {
        'Content-Type': 'application/json',
        'X-LINE-ChannelId': channel_id,
        }

    uri = "/v3/payments/request"
    nonce = str(round(time.time() * 1000))  # nonce = str(uuid.uuid4())
    headers['X-LINE-Authorization-Nonce'] = nonce
    transaction_id = None  # 初始化 transaction_id
    
    def get_auth_signature (secret, uri, body, nonce):
        """
        用於製作密鑰
        :param secret: your channel secret
        :param uri: uri
        :param body: request body
        :param nonce: uuid or timestamp(時間戳)
        :return:
        """
        
        # if None in [secret, uri, body, nonce]:
        #     raise ValueError("One of the arguments is None")
        str_sign = secret + uri + body + nonce

        return base64.b64encode(hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()).decode("utf-8")



    def do_request_payment():
        '''此api僅使用文檔中必填的資料'''
        request_options = {
            "amount": 1000, #linepay顯示-產品總價格
            "currency": 'TWD', #linepay顯示-幣別
            "orderId": nonce,
            "packages": [{
                "id": '20220314I001', #店家編號
                "amount": 1000, #linepay顯示-產品總價格
                "name": '六角棒棒堂商店',
                "products": [{
                    "name": '六角棒棒堂', #linepay顯示-產品名稱
                    "quantity": 1, #產品數量
                    "price": 1000  #產品價格
                },]
            }],
            "redirectUrls": {
                "confirmUrl": 'http://34.152.28.2/zh',
                "cancelUrl": 'https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/'
            }
        }
        json_body = json.dumps(request_options)

        
        headers['X-LINE-Authorization'] = get_auth_signature(str(channel_secret), str(uri), str(json_body), str(nonce))
        response = requests.post("https://sandbox-api-pay.line.me"+uri, headers=headers, data=json_body)
        print(response.text)
        dict_response = json.loads(response.text)

        if dict_response.get('returnCode') == "0000":
            info = dict_response.get('info')
            web_url = info.get('paymentUrl').get('web')
            transaction_id = str(info.get('transactionId'))
            print(f"付款web_url:{web_url}")
            print(f"交易序號:{transaction_id}")
        return web_url,transaction_id  # 返回 transaction_id

    def do_checkout(transaction_id):
        print("transaction_id={}".format(transaction_id))

        conf_data = """{"amount": 2000, "currency": "TWD"}"""
        checkout_url = f"/v3/payments/requests/{transaction_id}/check"
        headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, checkout_url, conf_data, nonce)
        response = requests.get("https://sandbox-api-pay.line.me"+checkout_url, headers=headers, data=conf_data)
        print(response.text)
        response = json.loads(response.text)
        if str(response.get('returnCode')) == "0110":
            return True
        return False

    def do_confirm(transaction_id):

        con_url = f"/v3/payments/{transaction_id}/confirm"
        conf_data = json.dumps({
                    "amount": amount,
                    "currency": currency
                    })
        headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, con_url, conf_data, nonce)
        response = requests.post("https://sandbox-api-pay.line.me"+con_url, headers=headers, data=conf_data)
        print(response.text)
        response = json.loads(response.text)

        return "Success" #response.get('returnMessage')
    
    # 在這裡呼叫 do_request_payment()
    
    # #非同步呼叫
    # async def main():
    #     transaction_id = await do_request_payment()
    #     if transaction_id:
    #         return {"message": "linepay success", "transaction_id": transaction_id}
    #     else:
    #         return {"message": "linepay fail"}, 400
    
    # await main()


    #同步呼叫
    # def main():
    web_url,transaction_id = do_request_payment()
    if web_url:
        return redirect(web_url, code=302)
        # return {"message_url": "linepay success", "web_url": web_url}
    else:
        return {"message_url": "linepay fail"},400
    # if transaction_id:
    #     return {"message": "linepay success", "transaction_id": transaction_id}
    # else:
    #     return {"message": "linepay fail"},400
    # status = do_checkout(transaction_id)
    # # if status:
    # #     return {"message": "linepay success", "status": status}
    # # else:
    # #     return {"message": "linepay_status fail"},400
    # if status == True:
    #     result = do_confirm(transaction_id)
    #     if result == "Success":  # 假設成功的訊息是"Success"
    #         return "Payment confirmed."
    #     else:
    #         return f"Payment failed with message: {result}"
    # else:
    #     return "Payment not verified."
        
        # return {"message": "linepay success"}

    # future = executor.submit(main)
    # return "Payment request received."

    # return jsonify({'channel_id': channel_id, 'status': 'success'})


