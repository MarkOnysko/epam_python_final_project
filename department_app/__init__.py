"""Module contains the app factory function"""
from flask import Flask
from flask_migrate import Migrate
from config import Config
from .models import db


migrate = Migrate()


def create_app(config_class=Config):
    """
    Function to create a Flask application instance with provided configuration.
    :param config_class: a class with configuration
    data to create the app instance with.
    :return: returns a Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from department_app.rest import api

        api.init_app(app)

    return app
