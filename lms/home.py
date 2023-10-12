from flask import Blueprint, redirect, render_template
from flask_login import current_user

home = Blueprint("home", __name__, template_folder="templates", static_folder="static")

@home.route('/', methods=["GET"])
def home_page():
    return render_template("home.html")
