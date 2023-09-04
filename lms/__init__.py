from flask import Flask, render_template
from lms.config import config
from lms.extensions import db, migrate, login_manager
from lms.auth import auth
from lms.home import home
from lms.librarian import librarian
from lms.student import student
from lms.admin import admin
from lms.models import Student, Librarian
from datetime import timedelta

 

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # setting up configuration from the development object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=5)


    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(librarian)
    app.register_blueprint(student)
    app.register_blueprint(admin)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    
      
    @login_manager.user_loader
    def load_user(id):
        user = Student.query.get(id)
        if user:
            return user
        else:
            return None
        
    @login_manager.user_loader
    def load_user(id):
        user = Librarian.query.get(id)
        if user:
            return user
        else:
            return None
    
     
    @app.errorhandler(404)
    def page_not_found(e):
        
        return render_template('auth/404.html')

    @app.errorhandler(500)
    def internal_server_error(e):
    
        return render_template('auth/500.html')

    return app
