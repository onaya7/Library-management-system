from flask import Blueprint, render_template, redirect


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@auth.route("/auth/admin/sign-in", methods=["GET","POST"])
def admin_sign_in():
    
    return render_template("auth/admin-sign-in.html")

@auth.route("/auth/librarian/sign-in", methods=["GET","POST"])
def librarian_sign_in():
    
    return render_template("auth/librarian-sign-in.html")

@auth.route("/auth/student/sign-in", methods=["GET","POST"])
def student_sign_in():
    
    return render_template("auth/student-sign-in.html")
    
