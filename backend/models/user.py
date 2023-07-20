from ..extentions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    native_lang = db.Column(db.String(10))
    line_id = db.Column(db.String(1000))

    def json(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            'mail': self.mail,
            'native_lang': self.native_lang,
            'line_id': self.line_id
        }