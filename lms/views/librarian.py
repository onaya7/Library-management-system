from flask import render_template, redirect
from flask_blueprint import Blueprint

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="static")

@librarian.route('/', methods=["GET"])
def home():
    return render_template('views/home.html')