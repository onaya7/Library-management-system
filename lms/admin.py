from flask import render_template, redirect
from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route('/admin/dashboard', methods=["GET"])
def dashboard():
    return render_template('admin/dashboard.html')