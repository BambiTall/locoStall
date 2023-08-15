from flask import Blueprint, Flask, request, jsonify, make_response
import os
import sys
from ..extentions import db
from ..models.shop import Shop
from ..models.menu import Menu
from ..models.menu_image import Menu_image
from ..models.shop_name import Shop_name

shop_bp = Blueprint('shop_bp', __name__)


# Get shop list
@shop_bp.route(f'{os.environ["API_BASE"]}/<lang>/shops', methods=['GET'])
def get_shop_list(lang):
    shop_data = []
    
    shops = Shop_name.query.filter_by(lang=lang).all()
    
    for shop in shops:
        shop_id = shop.shop_id
        shop_info = Shop.query.get(shop_id)
        
        shop_data.append({
            'shop_id': shop_id,
            'slug': shop_info.slug,
            'rating': shop_info.rating,
            'name': shop.name,
            'description': shop.description,
            'cover': shop_info.cover
        })
    
    return jsonify(shop_data)


# Get shop detail
@shop_bp.route(f'{os.environ["API_BASE"]}/<lang>/shop/<int:shop_id>', methods=['GET'])
def get_shop_detail(lang, shop_id):
    shop = Shop_name.query.filter_by(lang=lang, shop_id=shop_id).first()
    res = shop.json()

    # Add menu
    menus = Menu.query.filter_by(lang=lang, shop_id=shop_id)
    menu_list = [menu.json() for menu in menus]
    for menu in menu_list:
        try:
            image = Menu_image.query.filter_by(
                shop_id=shop_id, prod_id=menu["prod_id"]
            ).first()
            menu["image"] = image.url
        except:
            pass
    res["menu"] = menu_list

    # Add rating & cover
    shop_info = Shop.query.filter_by(id=shop_id).first()
    res["rating"] = shop_info.rating
    res["cover"] = shop_info.cover

    return res
