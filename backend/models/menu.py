from ..extentions import db

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    lang = db.Column(db.String(10))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'prod_id': self.prod_id,
            'lang': self.lang,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }