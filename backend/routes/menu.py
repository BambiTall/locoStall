from flask import Blueprint, Flask, request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
import os
from ..extentions import db
from ..models.menu import Menu

menu_bp = Blueprint('menu_bp', __name__)


# Get menu list
@menu_bp.route(f'{os.environ["API_BASE"]}/<lang>/menu/<int:shop_id>')
def get_menu_list(lang, shop_id):
    menus = Menu.query.filter_by(lang=lang, shop_id=shop_id)
    menu_list = [menu.json() for menu in menus]
    return {"data": menu_list}


# Get menu item
@menu_bp.route(f'{os.environ["API_BASE"]}/menu_item/<int:id>')
def get_menu_item(id):
    menu = db.get_or_404(entity=Menu, ident=id)
    return {"data": menu}
