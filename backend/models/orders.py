from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..extentions import db


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    item_list = db.Column(db.String(1000))
    payment = db.Column(db.String(20))
    state = db.Column(db.String(100))
    # waiting = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )
    paid = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'shop_id': self.shop_id,
            'item_list': self.item_list,
            'payment': self.payment,
            'state': self.state,
            # 'waiting': self.waiting,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'paid': self.paid,
        }
