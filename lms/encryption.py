import jwt
from flask import current_app


def generate_jwt(payload: dict, algorithm: str = "HS256") -> str:
    """
    Generates a JWT token from the given payload.
    """
    secret_key = current_app.config.get("SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_jwt(token: str, algorithm: str = "HS256") -> tuple:
    """
    Decodes a JWT token and returns the payload.
    """
    try:
        secret_key = current_app.config.get("SECRET_KEY")
        payload = jwt.decode(token.encode(), str(secret_key), algorithms=[algorithm])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Signature expired."
    except jwt.InvalidTokenError:
        return False, "Invalid token."
    except Exception as e:
        return False, str(e)

