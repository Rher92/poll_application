from poll_application.models import User


def get_user_by_email(email):
    return User.query.filter_by(email=email)

def get_user_by_username(username):
    return User.query.filter_by(username=username)