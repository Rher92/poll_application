import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .models import db as auth_db

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        auth_db.init_app(app)
        auth_db.create_all()

    from .auth.views import bp as auth_bp
    from .poll.views import bp as poll_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(poll_bp)

    return app