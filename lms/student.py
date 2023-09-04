from flask import Blueprint
from flask import render_template, redirect

student = Blueprint("student", __name__, template_folder="templates", static_folder="static")

@student.route('/student/dashboard', methods=["GET"])
def dashboard():
    return render_template('student/dashboard.html')