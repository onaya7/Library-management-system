from flask import render_template, redirect
from flask import Blueprint
from flask_login import login_required

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="assets")

@librarian.route('/librarian/dashboard', methods=["GET"])
@login_required
def dashboard():
    return render_template('librarian/dashboard.html')