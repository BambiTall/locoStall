from flask import (
    Blueprint,
    Flask,
    request,
    jsonify,
    make_response,
    session,
    redirect,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError
import os
import json
from ..extentions import db
from ..models.user import User

user_bp = Blueprint('user_bp', __name__)


# Get user list
@user_bp.route(f'{os.environ["API_BASE"]}/users')
def get_user_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return [user.json() for user in users]


# User log in
@user_bp.route(f'{os.environ["API_BASE"]}/user/login', methods=['POST'])
def user_log_in():
    data = request.get_json()

    db_user = User.query.filter_by(mail=data['mail']).first()
    if db_user is not None and db_user.password == data['password']:
        session['user_id'] = db_user.id
        session.permanent = True
        return {"id": db_user.id, "session_data": dict(session)}
    else:
        return {"message": "E-mail 或 password 錯誤"}, 400


# Get user detail
@user_bp.route(f'{os.environ["API_BASE"]}/user/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    # if user_id == session.get('user_id'):
    # if user_id in session:
    # user = db.get_or_404(User, user_id)
    db_user = User.query.filter_by(id=user_id).first()
    return db_user.json()


# else:
#     return {
#         "message": "用戶未登入"
#     }


# Add user
@user_bp.route(f'{os.environ["API_BASE"]}/user', methods=['POST'])
def add_web_user():
    data = request.get_json()
    db_user = User.query.filter_by(mail=data['mail']).first()
    if db_user is not None:
        return {"message": "E-mail 已註冊"}, 500
    else:
        user = User(
            mail=data['mail'], native_lang=data['nLang'], password=data['password']
        )
        db.session.add(user)
        db.session.commit()

        return {"data": user.json()}


# Update user datas
@user_bp.route(f'{os.environ["API_BASE"]}/user/<int:user_id>', methods=['POST'])
def update_user_datas(user_id):
    data = request.get_json()
    user = db.get_or_404(entity=User, ident=user_id)
    user.display_name = (
        data['display_name'] if data['display_name'] else user.display_name
    )
    user.mail = data['mail'] if data['mail'] else user.mail
    user.native_lang = data['native_lang'] if data['native_lang'] else user.native_lang
    user.line_id = data['line_id'] if data['line_id'] else user.line_id
    user.password = data['password'] if data['password'] else user.password
    user.type = data['type'] if data['type'] else user.type
    user.shop_id = data['shop_id'] if data['shop_id'] else user.shop_id

    db.session.commit()

    return {"data": user.json()}
