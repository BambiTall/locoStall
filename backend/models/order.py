from ..extentions import db

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    order_list = db.Column(db.String(1000))
    payment = db.Column(db.String(20))
    create_at = db.Column(db.String(50))
    update_at = db.Column(db.String(50))
    
    def json(self):
	    return {
            'id': self.id,
            'user_id': self.user_id,
            'shop_id': self.shop_id,
            'order_list': self.order_list,
            'payment': self.payment,
            'create_at': self.create_at,
            'update_at': self.update_at,
		}
    