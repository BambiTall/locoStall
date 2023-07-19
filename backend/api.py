from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{environ["DB_USER"]}:{environ["DB_PWD"]}@{environ["DB_HOST"]}:{environ["DB_PORT"]}/{environ["DB_NAME"]}'

db.init_app(app)

api_base = '/api/'

class User(db.Model):
    # __tablename__ = 'user'

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


# get all users
@app.route(api_base + '/users', methods=['GET'])
def get_users():
  try:
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return [user.json() for user in users]
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# with app.app_context():
#   db.create_all()

@app.route( '/' )
def api_ready():
    return 'api ready!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')