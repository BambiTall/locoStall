from ..extentions import db
from .shop import Shop

class Shop_name(db.Model):
    __tablename__ = 'shop_name'

    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    lang = db.Column(db.String(10))
    name = db.Column(db.String(20))
    description = db.Column(db.String(500))

    def json(self):
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'lang': self.lang,
            'name': self.name,
            'description': self.description,
        }