from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

database = SQLAlchemy()

from .security import authentication
from .sql_struct import User, Note 
from .notes import notelist

def database_maker(web):
    if path.exists('Website/' + "site_database.db"):
        None
    elif not path.exists('Website/' + "site_database.db"):
        database.create_all(app=web)

def site_setup():
    #import blueprint
    flask_instance = Flask(__name__)
    flask_instance.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{"site_database.db"}'
    flask_instance.config['SECRET_KEY'] = 'HIDDEN' #encrypts the cookie and session data
    database.init_app(flask_instance)
    #register blueprints
    flask_instance.register_blueprint(authentication, url_prefix='/')
    flask_instance.register_blueprint(notelist, url_prefix='/')
    database_maker(flask_instance)

    login = LoginManager()
    login.login_view = 'authentication.user_login'
    login.init_app(flask_instance)
    @login.user_loader
    def get_user(id):
        user_id = int(id)
        return User.query.get(user_id)

    return flask_instance
