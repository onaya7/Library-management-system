from flask_blueprint import Blueprint


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")
