from flask import Blueprint
from flask import render_template, redirect

student = Blueprint("student", __name__, template_folder="templates", static_folder="static")

# @student.route('/view/student', methods=["GET"])
# def view_student():
#     return render_template('views/home.html')