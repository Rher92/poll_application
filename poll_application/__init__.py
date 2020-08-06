import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_object(os.environ['APP_SETTINGS'])

    with app.app_context():
        db.init_app(app)

    from .auth.views import bp as auth_bp
    from .poll.views import bp as poll_bp
    from .ping.views import bp as ping_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(poll_bp)
    app.register_blueprint(ping_bp)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}    

    return app