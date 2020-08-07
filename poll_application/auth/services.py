from poll_application import db
from poll_application.auth.models import User
from poll_application.poll.models import Poll, Question, Answer, Tag
from werkzeug.security import generate_password_hash

def create_user(username, email, password):
    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()


def save_user(user):
    db.session.add(user)
    db.session.commit()