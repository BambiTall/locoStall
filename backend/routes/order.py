from flask import Blueprint, Flask, request, jsonify, make_response
import os
from ..extentions import db
from ..models.order import Order
from ..models.shop_name import Shop_name
from ..models.user import User

order_bp = Blueprint('order_bp', __name__)


# Add order
@order_bp.route(f'{os.environ["API_BASE"]}/order', methods=['POST'])
def add_order():
    data = request.get_json()
    db_shop = Shop_name.query.filter_by(shop_id=data['shop_id']).first()
    db_user = User.query.filter_by(id=data['user_id']).first()
    if db_shop and db_user:
        order = Order(
            user_id=data['user_id'],
            shop_id=data['shop_id'],
            order_list=data['order_list'],
            payment=data['payment'],
            create_at=data['create_at'],
            update_at=data['update_at'],
        )
        db.session.add(order)
        db.session.commit()
        return True
    else:
        return False
