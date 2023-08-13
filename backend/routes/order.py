from flask import Blueprint, Flask, request, jsonify, make_response
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
    order.waiting = data['waiting']
    db.session.commit()

    return {'message': 'Order state updated successfully'}, 200
