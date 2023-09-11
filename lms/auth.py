from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from lms.extensions import bcrypt
from lms.forms import AdminLoginForm, LibrarianLoginForm, StudentLoginForm
from lms.models import Librarian, Student

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="assets")


@auth.route("/auth/student/sign-in", methods=["GET", "POST"])
def student_sign_in():
    form = StudentLoginForm()
    if form.validate_on_submit():
        matric_no = form.matric_no.data.lower().strip()
        password = form.password.data.lower().strip()
        remember = form.remember.data.lower().strip()

        user = Student.query.filter_by(matric_no=matric_no).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                flash("logged in successfully", "success")
                next_page = request.args.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("student.dashboard"))
                )
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
        email = form.email.data.lower().strip()
        password = form.password.data.lower().strip()
        remember = form.remember.data

        user = Librarian.query.filter_by(email=email).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                flash("logged in successfully", "success")
                next_page = request.args.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("librarian.dashboard"))
                )
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

        user = Librarian.query.filter_by(email=email).first()
        if user is not None and user.is_admin is True:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                flash("logged in successfully", "success")
                next_page = request.args.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("admin.dashboard"))
                )
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
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.student_sign_in"))


@auth.route("/auth/librarian/logout", methods=["GET", "POST"])
@login_required
def logout_librarian():
    logout_user()
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.librarian_sign_in"))


@auth.route("/auth/admin/logout", methods=["GET", "POST"])
@login_required
def logout_admin():
    logout_user()
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.admin_sign_in"))
