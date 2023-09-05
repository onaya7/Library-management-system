from flask import Blueprint, render_template, redirect, flash, request, url_for
from lms.forms import AdminLoginForm, StudentLoginForm, LibrarianLoginForm
from lms.models import Student, Librarian
from lms.extensions import bcrypt
from flask_login import login_required, login_user, logout_user, current_user


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
                flash('logged in successfully', "success")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('student.dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', "danger")
        else:
            flash('Login Unsuccessful. Please check username and password', "danger")
    return render_template("auth/student-sign-in.html", form=form)


@auth.route("/auth/librarian/sign-in", methods=["GET", "POST"])
def librarian_sign_in():
    form = LibrarianLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = Librarian.query.filter_by(email=email).first()
        if user is not None:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                flash('logged in successfully', "success")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('librarian.dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', "danger")
        else:
            flash('Login Unsuccessful. Please check username and password', "danger")
    return render_template("auth/librarian-sign-in.html", form=form)


@auth.route("/auth/admin/sign-in", methods=["GET", "POST"])
def admin_sign_in():
    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        
        user = Librarian.query.filter_by(email=email).first()
        if user is not None and user.is_admin is True:
            user_password = user.password
            password_check = bcrypt.check_password_hash(user_password, password)
            if password_check:
                login_user(user, remember=remember)
                flash('logged in successfully', "success")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', "danger")
        else:
            flash('Login Unsuccessful. Please check username and password', "danger")
    return render_template("auth/admin-sign-in.html", form=form)


@auth.route("/auth/logout", methods=["GET", "POST"])
@login_required
def logout_student():
    logout_user()
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.student_sign_in"))


@auth.route("/auth/logout", methods=["GET", "POST"])
@login_required
def logout_librarian():
    logout_user()
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.librarian_sign_in"))


@auth.route("/auth/logout", methods=["GET", "POST"])
@login_required
def logout_admin():
    logout_user()
    flash("logged out successfully.", "danger")
    return redirect(url_for("auth.admin_sign_in"))