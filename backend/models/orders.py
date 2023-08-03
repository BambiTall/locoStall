from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..extentions import db

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(11))
    shop_id = db.Column(db.String(11))
    order_list = db.Column(db.String(1000))
    payment = db.Column(db.String(20))
    state = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=db.func.now(), server_onupdate=db.func.now())
    

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'shop_id': self.shop_id,
            'order_list': self.order_list,
            'payment': self.payment,
            'state': self.state,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }