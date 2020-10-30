# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_migrate import Migrate, MigrateCommand

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app(config_file):
    app = Flask(__name__)
    alchemy_engine = "postgresql://{}:{}@{}:5432/{}".format(config_file['user'], config_file['password'], config_file['host'], config_file['db_name'])


    app.config['SQLALCHEMY_DATABASE_URI'] = alchemy_engine

    db.init_app(app)
    Migrate(db,app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
