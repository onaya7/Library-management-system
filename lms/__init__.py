from flask import Flask
from lms.config import config
from lms.extensions import db, migrate
from lms.auth import auth
from lms.home import home
from lms.librarian import librarian
from lms.student import student
 

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # setting up configuration from the development object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(librarian)
    app.register_blueprint(student)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    return app
