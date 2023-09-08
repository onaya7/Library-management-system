from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def session_expired_handler(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Session has expired, please login to access this page', 'danger')
                return redirect(url_for(f'auth.{role}_sign_in'))
    
            return func(*args, **kwargs)
        
        return decorated_function
    return decorator


