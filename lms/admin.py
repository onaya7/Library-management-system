from flask import render_template, redirect
from flask import Blueprint
from flask_login import login_required
from lms.decorator import session_expired_handler

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="assets")

@admin.route('/admin/dashboard', methods=["GET"])
@session_expired_handler('admin')
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/admin/edit_student', methods=["GET", "POST"])
@session_expired_handler('admin')
def edit_student():
    return render_template('admin/edit_student.html')


@admin.route('/admin/edit_librarian', methods=["GET", "POST"])
@session_expired_handler('admin')
def edit_librarian():
    return render_template('admin/edit_librarian.html')