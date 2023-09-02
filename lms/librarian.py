from flask import render_template, redirect
from flask import Blueprint

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="static")

@librarian.route('/view/librarian', methods=["GET"])
def librarian():
    return render_template("views/home.html")