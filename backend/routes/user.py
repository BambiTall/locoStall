from flask import Blueprint, Flask, request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
import os
from ..extentions import db
from ..models.user import User

user_bp = Blueprint('user_bp', __name__)

# Get user list
@user_bp.route(f'{os.environ["API_BASE"]}/users')
def get_user_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return [user.json() for user in users]

# Get user detail
@user_bp.route(f'{os.environ["API_BASE"]}/user/<int:user_id>', methods=['GET', 'POST'])
def get_user_detail(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "data" : user.json()
    }

# Add user
@user_bp.route(f'{os.environ["API_BASE"]}/user', methods=['POST'])
def add_web_user():
    data = request.get_json()
    db_user = User.query.filter_by(mail=data['mail']).first()
    if db_user is not None:
        return {
            "message": "E-mail 已註冊"
        }, 500
    else:
        user = User(
            mail = data['mail'],
            native_lang = data['nLang'],
            password = data['password']
        )
        db.session.add(user)
        db.session.commit()

        return {
            "data" : user.json()
        }

# User log in
@user_bp.route(f'{os.environ["API_BASE"]}/user/login', methods=['POST'])
def user_log_in():
    data = request.get_json()
    
    db_user = User.query.filter_by(mail=data['mail']).first()
    if db_user is not None and db_user.password == data['password']:
        return {
            "message" :  "Success"
        }
    else:
        return {
            "message": "E-mail 或 password 錯誤"
        }, 400