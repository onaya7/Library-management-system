from flask import Flask
from lms.config import config
from lms.extensions import db, migrate, login_manager
from lms.auth import auth
from lms.home import home
from lms.librarian import librarian
from lms.student import student
from lms.admin import admin
from lms.models import Student, Librarian

 

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # setting up configuration from the development object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(librarian)
    app.register_blueprint(student)
    app.register_blueprint(admin)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    
      
    @login_manager.user_loader
    def load_user(user_id):
        user = Student.query.get(user_id)
        if user:
            return user
        else:
            return None
        
    @login_manager.user_loader
    def load_user(user_id):
        user = Librarian.query.get(user_id)
        if user:
            return user
        else:
            return None

    return app
