from flask import Blueprint, Flask, request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
import os
import json
from sqlalchemy.sql import func
from ..extentions import db
from ..models.orders import Orders
from ..models.menu import Menu
from ..models.shop_name import Shop_name

order_bp = Blueprint('order_bp', __name__)


# Get orders list
@order_bp.route(f'{os.environ["API_BASE"]}/orders')
def get_orders_list():
    orders_list = db.session.execute(db.select(Orders).order_by(Orders.id)).scalars()

    return [orders.json() for orders in orders_list]


# Get orders detail
@order_bp.route(
    f'{os.environ["API_BASE"]}/order_detail/<int:order_id>', methods=['GET']
)
def get_orders_detail(order_id):
    order = db.get_or_404(Orders, order_id)

    return {"data": order.json()}


# Add order
@order_bp.route(f'{os.environ["API_BASE"]}/send_order', methods=['POST'])
def add_order():
    data = request.get_json()

    order_list_json = json.dumps(data['order_list'])

    orders = Orders(
        order_list=order_list_json,
        user_id=data['user_id'],
        payment=data['payment'],
        shop_id=data['shop_id'],
    )

    db.session.add(orders)
    db.session.commit()

    return {"message": "送出訂單成功", "data": orders.json()}
