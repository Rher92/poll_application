from poll_application.models import User, db, Poll, Question, Answer
from werkzeug.security import generate_password_hash

def create_user(username, email, password):
    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()     