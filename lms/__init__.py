import os
from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_uploads import configure_uploads


from lms.admin import admin
from lms.auth import auth
from lms.config import config
from lms.extensions import db, login_manager, migrate
from lms.forms import images
from lms.helpers import token_authentication
from lms.home import home
from lms.librarian import librarian
from lms.student import student


def create_app(config_name="development"):
    app = Flask(__name__)

    # setting up configuration from the development object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config["SESSION_TYPE"] = "filesystem"

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=1)

    # flask_uploads
    app.config["UPLOADED_IMAGES_DEST"] = os.path.join(app.root_path, "upload")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    configure_uploads(app, images)

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(librarian)
    app.register_blueprint(student)
    app.register_blueprint(admin)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized_user():
        if request.endpoint == "auth.logout_student":
            flash("Sorry only students are authorized to access this page.", "danger")
            return redirect(url_for("auth.student_sign_in"))

        elif request.endpoint == "auth.logout_librarian":
            flash("Sorry only librarians are authorized to access this page.", "danger")
            return redirect(url_for("auth.librarian_sign_in"))

        elif request.endpoint == "auth.logout_admin":
            flash("Sorry only admins are authorized to access this page.", "danger")
            return redirect(url_for("auth.admin_sign_in"))

    # Custom request loader to get user based on session ID
    @login_manager.request_loader
    def load_user_from_request(request):
        user = token_authentication(request)
        return user

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("auth/404.html")

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("auth/500.html")

    with app.app_context():
        pass

    return app
