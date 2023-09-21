from flask import make_response

from lms.encryption import decode_jwt
from lms.models import Librarian, Student

#function to handle the login token
def handle_login(token):
    ok, data = decode_jwt(token)

    if ok:
        role = data.get("role")
        alternative_id = data.get("id")

        if role == "admin":
            admin = Librarian.query.filter_by(
                alternative_id=alternative_id, is_admin=True
            ).first()
            if admin:
                return admin

        elif role == "librarian":
            librarian = Librarian.query.filter(
                Librarian.alternative_id == alternative_id,
                Librarian.is_librarian == True,
            ).first()
            if librarian:
                return librarian

        elif role == "student":
            student = Student.query.filter_by(alternative_id=alternative_id).first()
            if student:
                return student

    return None

#function to handle the token authentication
def token_authentication(request) -> str:
    # check for the cookie token
    cookie_token = request.cookies.get("token")
    if cookie_token:
        return handle_login(cookie_token)


def set_cookie(response: make_response, token, duration=3600) -> make_response:
    cookie = dict()

    cookie["key"] = "token"
    cookie["value"] = token
    cookie["max_age"] = duration

    response.set_cookie(**cookie)
    return response
