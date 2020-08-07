from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from secrets import token_hex

from poll_application import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(32), unique=True)
    token = db.Column(db.String(32), 
        unique=True,
        default=token_hex(16))
    poll = db.relationship('Poll', 
        backref='author', 
        lazy=True)
    created_at = db.Column(db.DateTime(), 
        nullable=False, 
        default=db.func.current_timestamp())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        return f'{self.username}'
