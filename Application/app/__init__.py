from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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

    return app
