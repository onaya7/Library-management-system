from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app
)
from flask_login import login_required, login_user, logout_user

from lms.extensions import bcrypt
from lms.forms import AdminLoginForm, LibrarianLoginForm, StudentLoginForm
from lms.helpers import set_cookie, generate_library_card
from lms.models import Librarian, Student


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="assets")


@auth.route("/auth/student/sign-in", methods=["GET", "POST"])
def student_sign_in():
    form = StudentLoginForm()
    if form.validate_on_submit():
        matric_no = form.matric_no.data
        password = form.password.data
        remember = form.remember.data

        user = Student.query.filter_by(matric_no=matric_no).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                token = user.generate_jwt()

                # Create a response object and set the cookie
                response = make_response(redirect(url_for("student.dashboard")))
                response = set_cookie(response, token)
                # Handle 'next' query parameter
                next_page = request.args.get("next")
                if next_page:
                    flash("Logged in successfully", "success")
                    return response

                # Flash message when redirecting to the next page
                flash("Logged in successfully", "success")

                return response

            else:
                flash(
                    "Login Unsuccessful. Please check username and password", "danger"
                )
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("auth/student-sign-in.html", form=form)


@auth.route("/auth/librarian/sign-in", methods=["GET", "POST"])
def librarian_sign_in():
    form = LibrarianLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = Librarian.query.filter_by(email=email, is_librarian=True).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                token = user.generate_jwt()

                # Create a response object and set the cookie
                response = make_response(redirect(url_for("librarian.dashboard")))
                response = set_cookie(response, token)
                # Handle 'next' query parameter
                next_page = request.args.get("next")
                if next_page:
                    flash("Logged in successfully", "success")
                    return response

                # Flash message when redirecting to the next page
                flash("Logged in successfully", "success")

                return response

            else:
                flash(
                    "Login Unsuccessful. Please check username and password", "danger"
                )
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("auth/librarian-sign-in.html", form=form)


@auth.route("/auth/admin/sign-in", methods=["GET", "POST"])
def admin_sign_in():
    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data.lower().strip()
        remember = form.remember.data

        user = Librarian.query.filter_by(email=email, is_admin=True).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                token = user.generate_jwt()

                # Create a response object and set the cookie
                response = make_response(redirect(url_for("librarian.dashboard")))
                response = set_cookie(response, token)
                # Handle 'next' query parameter
                next_page = request.args.get("next")
                if next_page:
                    flash("Logged in successfully", "success")
                    return response

                # Flash message when redirecting to the next page
                flash("Logged in successfully", "success")

                return response

            else:
                flash(
                    "Login Unsuccessful. Please check username and password", "danger"
                )
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("auth/admin-sign-in.html", form=form)


@auth.route("/auth/student/logout", methods=["GET", "POST"])
@login_required
def logout_student():
    logout_user()
      # Create a response object and remove the token cookie
    response = make_response(redirect(url_for("auth.student_sign_in")))
    response.set_cookie("token", "", expires=0)

    flash("Logged out successfully.", "success")
    return response


@auth.route("/auth/librarian/logout", methods=["GET", "POST"])
@login_required
def logout_librarian():
    logout_user()
    # Create a response object and remove the token cookie
    response = make_response(redirect(url_for("auth.librarian_sign_in")))
    response.set_cookie("token", "", expires=0)

    flash("Logged out successfully.", "success")
    return response


@auth.route("/auth/admin/logout", methods=["GET", "POST"])
@login_required
def logout_admin():
    logout_user()
      # Create a response object and remove the token cookie
    response = make_response(redirect(url_for("auth.admin_sign_in")))
    response.set_cookie("token", "", expires=0)

    flash("Logged out successfully.", "success")
    return response