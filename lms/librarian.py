from flask import render_template, redirect
from flask import Blueprint

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="static")

@librarian.route('/librarian/dashboard', methods=["GET"])
def dashboard():
    return render_template('views/dashboard.html')