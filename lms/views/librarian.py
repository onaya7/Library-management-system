from flask_blueprint import Blueprint

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")
