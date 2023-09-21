from flask import Blueprint, redirect, render_template
from flask_login import login_required

from lms.decorator import session_expired_handler, role_required

admin = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="assets"
)


@admin.route("/admin/dashboard", methods=["GET"])
@session_expired_handler("admin")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@admin.route("/admin/edit_student", methods=["GET", "POST"])
@session_expired_handler("admin")
@login_required
def edit_student():
    return render_template("admin/edit_student.html")


@admin.route("/admin/edit_librarian", methods=["GET", "POST"])
@session_expired_handler("admin")
@login_required
def edit_librarian():
    return render_template("admin/edit_librarian.html")
