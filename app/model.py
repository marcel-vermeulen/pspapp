from flask import current_app
from flask_login import UserMixin
import jwt
from time import time
from datetime import datetime

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = 'pspusers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(40), unique=False)
    surname = db.Column(db.String(40), unique=False, nullable=True)
    mobile = db.Column(db.String(10), unique=True, nullable=True, default="0000000000")   
    ipam = db.Column(db.String(40), unique=False, nullable=False)
    created = db.Column(db.DateTime, index=False, default=datetime.now())   
    is_active = db.Column(db.Boolean,default = True)
    lastlogon = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

