from flask_blueprint import Blueprint

student = Blueprint("student", __name__, template_folder="templates", static_folder="static")
