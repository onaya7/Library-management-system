from flask_blueprint import Blueprint
from flask import render_template, redirect

student = Blueprint("student", __name__, template_folder="templates", static_folder="static")

@student.route('/', methods=["GET"])
def home():
    return render_template('views/home.html')