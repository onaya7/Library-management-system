from flask import Blueprint, render_template, redirect


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@auth.route("/auth/sign-in", methods=["GET","POST"])
def sign_in():
    return render_template("auth/sign-in.html")
    
