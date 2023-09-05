from flask import Blueprint
from flask import render_template, redirect
from flask_login import login_required

student = Blueprint("student", __name__, template_folder="templates", static_folder="assets")

@student.route('/student/dashboard', methods=["GET"])
@login_required
def dashboard():
    return render_template('student/dashboard.html')