from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

from config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bcrypt.init_app(app)
    login.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        from app.main.routes import main
        app.register_blueprint(main)

        from app.auth.routes import auth
        app.register_blueprint(auth)

        from app.ipam.routes import ipam
        app.register_blueprint(ipam)

        return app

from app import model
