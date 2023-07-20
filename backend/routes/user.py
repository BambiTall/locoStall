from flask import Blueprint, Flask, request, jsonify, make_response
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
    return { "message" : "OK", "data" : user.json() }