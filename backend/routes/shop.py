from flask import Blueprint, Flask, request, jsonify, make_response
import os
import sys
from ..extentions import db
from ..models.shop import Shop
from ..models.menu import Menu
from ..models.shop_name import Shop_name

shop_bp = Blueprint('shop_bp', __name__)

# Get shop list
@shop_bp.route(f'{os.environ["API_BASE"]}/<lang>/shops', methods=['GET'])
def get_shop_list(lang):
    shops = Shop_name.query.filter_by(lang=lang)
    shop_list = [shop.json() for shop in shops]
    return jsonify(shop_list)

# Get shop detail
@shop_bp.route(f'{os.environ["API_BASE"]}/<lang>/shop/<int:shop_id>', methods=['GET'])
def get_shop_detail(lang, shop_id):
    shop = Shop_name.query.filter_by(lang=lang, shop_id=shop_id).first()
    res = shop.json()

    # Add menu
    menus = Menu.query.filter_by(lang=lang, shop_id=shop_id)
    menu_list = [menu.json() for menu in menus]
    res["menu"] = menu_list

    # Add rating
    shop_info = Shop.query.filter_by(id=shop_id).first()
    res["rating"] = shop_info.rating

    return res