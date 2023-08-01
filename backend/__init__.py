from flask import Flask
from flask_cors import CORS
import os
from .extentions import db

# import blueprint
from .routes.user import user_bp
from .routes.shop import shop_bp
from .routes.order import order_bp
from .routes.menu import menu_bp
from .routes.predict import predict_bp


def create_app():
    app = Flask(__name__)

    # db setting
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'mysql+pymysql://{os.environ["DB_USER"]}:{os.environ["DB_PWD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    # register blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(predict_bp)

    db.init_app(app)
    CORS(app)

    return app
