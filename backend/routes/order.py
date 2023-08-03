from flask import Blueprint, Flask, request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import json
from sqlalchemy.sql import func
from ..extentions import db
from ..models.orders import Orders
from ..models.menu import Menu
from ..models.shop_name import Shop_name

order_bp = Blueprint('order_bp', __name__)


# Get order list
@order_bp.route(f'{os.environ["API_BASE"]}/orders')
def get_orders_list():
    order_list = db.session.execute(db.select(Orders).order_by(Orders.id)).scalars()

    return [orders.json() for orders in order_list]


# Get user orders
@order_bp.route(f'{os.environ["API_BASE"]}/orders/user/<int:user_id>')
def get_user_order_list(user_id):
    orders = Orders.query.filter_by(user_id=user_id)
    order_list = [order.json for order in orders]

    return jsonify(order_list)


# Get shop orders
@order_bp.route(f'{os.environ["API_BASE"]}/orders/shop/<int:shop_id>')
def get_user_order_list(shop_id):
    orders = Orders.query.filter_by(shop_id=shop_id)
    order_list = [order.json for order in orders]

    return jsonify(order_list)


# Get order detail
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


# Update order (require datas : order's id, state)
@order_bp.route(f'{os.environ["API_BASE"]}/update_order', methods=['POST'])
def update_order():
    data = request.get_json()
    order = db.get_or_404(entity=Orders, ident=data['id'])
    order.state = data['state'] if data['state'] else order.state
    order.updated_at = datetime.utcnow

    return {'message': 'Order state updated successfully'}, 200
