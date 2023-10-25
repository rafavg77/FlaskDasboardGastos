from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

from .config.config import ProductionConfig, DevelopmentConfig, TestingConfig

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

    if app.config['FLASK_ENV'] == 'production':
        app.config.from_object(ProductionConfig)
    elif app.config['FLASK_ENV'] == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    db.init_app(app)

    #Importar blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from .accounts import account_bp
    app.register_blueprint(account_bp)


    return app