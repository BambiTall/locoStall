from flask import Flask
from flask_cors import CORS
import os
from .extentions import db

from dotenv import load_dotenv
load_dotenv()

# import blueprint
from .routes.user import user_bp
from .routes.shop import shop_bp
from .routes.orders import orders_bp
from .routes.menu import menu_bp
from .routes.linebot import linebot_bp

def create_app():
    app = Flask(__name__)

    # db setting
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PWD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    
    # register blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(linebot_bp)

    db.init_app(app)
    CORS(app)
    
    return app