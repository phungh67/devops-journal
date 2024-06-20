from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config

db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # temporary route for tésting purpose only, or you can keep it
    @app.route('/')
    def hello_world():
        return "Hello, World!"
    
    # call the login manager extension

    login_manager.init_app(app)
    login_manager.login_message = "You must been logged in to view this content."
    login_manager.login_view = "auth.login"

    # create the migration process 

    migrate = Migrate(app, db)

    Bootstrap(app)
    
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)


    return app
