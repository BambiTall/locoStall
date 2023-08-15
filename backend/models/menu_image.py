from ..extentions import db


class Menu_image(db.Model):
    __tablename__ = 'menu_image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    shop_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
