from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from secrets import token_hex

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('poll_id', db.Integer, db.ForeignKey('polls.id'), primary_key=True)
)    

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    token = db.Column(db.String(16), 
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

    def __repr__(self):
        return '{}'.format(self.username)



class Poll(db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, \
        db.ForeignKey('users.id'), \
        nullable=False)
    questions = db.relationship('Question', 
        backref='poll', 
        lazy=True)
    tags = db.relationship('Tag', 
        secondary=tags, 
        lazy='subquery',
        backref=db.backref('pages', lazy=True))
    created_at = db.Column(db.DateTime(), 
        nullable=False, 
        default=db.func.current_timestamp())
    close_date = db.Column(db.DateTime(), 
        nullable=False)

    def __init__(self, title, user_id, close_date):
        self.title = title
        self.user_id = user_id
        self.close_date = close_date

    def __repr__(self):
        return '{}'.format(self.title)      


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    _question = db.Column(db.String(100), unique=False, nullable=False)
    poll_id = db.Column(db.Integer, \
        db.ForeignKey('polls.id'), \
        nullable=False)
    answer = db.relationship('Answer', 
        backref='question', 
        lazy=True)
    counter = db.Column(db.Integer,
        default=0)
    created_at = db.Column(db.DateTime(), 
        nullable=False, 
        default=db.func.current_timestamp())    

    def __init__(self, question, poll_id):
        self._question = question
        self.poll_id = poll_id

    def __repr__(self):
        return '{}'.format(self._question)


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    _answer = db.Column(db.String(100), unique=False, nullable=False)
    question_id = db.Column(db.Integer, \
        db.ForeignKey('questions.id'), \
        nullable=False)
    created_at = db.Column(db.DateTime(), 
        nullable=False, 
        default=db.func.current_timestamp())        

    def __init__(self, _answer, question_id):
        self._answer = _answer
        self.question_id = question_id

    def __repr__(self):
        return '{}'.format(self._answer)    


class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), 
        unique=True, 
        nullable=True)
    created_at = db.Column(db.DateTime(), 
        nullable=True, 
        default=db.func.current_timestamp())        

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '{}'.format(self.title)    