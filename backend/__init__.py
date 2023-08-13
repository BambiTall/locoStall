from flask import Flask
from flask_cors import CORS
import os
from .extentions import db
from datetime import timedelta
from flask.sessions import SecureCookieSessionInterface

from dotenv import load_dotenv

load_dotenv()

# import blueprint
from .routes.user import user_bp
from .routes.shop import shop_bp
from .routes.order import order_bp
from .routes.menu import menu_bp
# from .routes.linebot import linebot_bp
from .routes.predict import predict_bp


def create_app():
    app = Flask(__name__)

    # db setting
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'mysql+pymysql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PWD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SECRET_KEY']  = f'{os.environ.get("FLASK_SCREAT_KEY")}'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)


    # register blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(menu_bp)
    # app.register_blueprint(linebot_bp)
    app.register_blueprint(predict_bp)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    return app
