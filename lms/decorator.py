from functools import wraps

from flask import flash, redirect, request, url_for
from flask_login import current_user

from lms.encryption import decode_jwt

#custom decorator for session-expired-handling
def session_expired_handler(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You are not logged in", "danger")
                return redirect(url_for(f"auth.{role}_sign_in"))

            return func(*args, **kwargs)

        return decorated_function

    return decorator


# custom decorator for role-based access control
def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("token", "")

            ok, data = decode_jwt(token)

            if ok:
                role = data.get("role")

                if role in allowed_roles:
                    return func(*args, **kwargs)
                else:
                    flash(
                        f"Access denied. You do not have permission to access this page",
                        "danger",
                    )
            else:
                flash(
                    f"Access denied. You do not have permission to access this page",
                    "danger",
                )

            return redirect(url_for(f"auth.{allowed_roles}_sign_in"))

        return wrapper

    return decorator
