# from functools import wraps
# from flask_login import current_user

# def check_confirmed(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):        
#         if current_user.is_admin == False:
#             flash('Please confirm your email address', 'danger')
#             return redirect(url_for('auth.unconfirmed'))
        
#         return func(*args, **kwargs)
        
#     return decorated_function
