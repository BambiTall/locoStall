from ..extentions import db


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    shop_names = db.relationship('Shop_name', backref='shop', lazy=True)
    cover = db.Column(db.String(255))

    def json(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'rating': self.rating,
            'shop_names': [shop_name.json() for shop_name in self.shop_names],
            'cover': self.cover,
        }
