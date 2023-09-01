from flask_blueprint import Blueprint
from flask import render_template, redirect


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@auth.route('/auth/sign_in', methods=["GET"])
def sign_in():
    return render_template('auth/sign-in.html')
@auth.route('/auth/sign_up', methods=["GET"])
def sign_up():
    return render_template('auth/sign-up.html')