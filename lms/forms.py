from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)
from lms.models import Librarian, Student


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(min=6, max=35, message="Little short for an email address?"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Password must match confirm password"),
            Length(min=5, max=50, message="Password is too short"),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\#])[A-Za-z\d@$!%*?&\#]+$",
                message="Password must include at least one uppercase letter, one lowercase letter, one number, and one special character",
            ),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")

    # def validate_username(self, username):
    #     librarian = Librarian.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError("This username is already in use by another user")

    # def validate_email(self, email):
    #     user = Librarian.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError("This email is taken. Please choose a different one")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(min=6, max=35, message="Little short for an email address?"),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

