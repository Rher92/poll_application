from poll_application.models import User, db, Poll, \
    Question, Answer, Tag

def get_user(username):
    return User.query.filter_by(username=username).first()

