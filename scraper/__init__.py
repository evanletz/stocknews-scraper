from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from scraper.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # 'login' -> function name of the route
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config=Config):
    '''
    Create an application template.
    '''
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from scraper.main.routes import main
    from scraper.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
