from ..extentions import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(500))
    display_name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    native_lang = db.Column(db.String(10), default='en')
    line_id = db.Column(db.String(1000))
    password = db.Column(db.String(50))
    type = db.Column(db.String(20), default='user')
    shop_id = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'photo': self.photo,
            'display_name': self.display_name,
            'mail': self.mail,
            'native_lang': self.native_lang,
            'line_id': self.line_id,
            'password': self.password,
            'type': self.type,
            'shop_id': self.shop_id,
        }
