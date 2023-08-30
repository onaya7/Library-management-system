from flask import Flask
from lms.config import config
from lms.extensions import db, migrate


def create_app(config_name="development"):
    app = Flask(__name__)

    # setting up configuration from the development object
    app.config.from_object(config[config_name])
    configuration = config[config_name]
    configuration.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    return app
