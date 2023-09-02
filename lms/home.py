from flask import Blueprint
from flask import redirect, render_template

home = Blueprint("home", __name__, template_folder="templates", static_folder="static")

# @home.route('/', methods=["GET"])
# def home():
#     return render_template("views/home.html")



