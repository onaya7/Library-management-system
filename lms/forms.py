from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)
from lms.models import Librarian, Student, BookCategory, Author


class StudentLoginForm(FlaskForm):
    matric_no = StringField(
        "Matric number",
        validators=[
            DataRequired(),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign in")
    
class LibrarianLoginForm(FlaskForm):
    email = EmailField(
        "Email address",
        validators=[
            DataRequired(),
            Email(),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    
    
class AdminLoginForm(FlaskForm):
    email = EmailField(
        "Email address",
        validators=[
            DataRequired(),
            Email(),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    


class AuthorForm(FlaskForm):
    name = StringField("Author name", validators=[DataRequired()])
    submit = SubmitField("Save Author")

    
    def validate_name(self, name):
        author = Author.query.filter_by(name=name.data).first()
        if author:
            raise ValidationError(f"This name {author.name} already exist as an Author please use a different one")



class BookCategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired()])
    submit = SubmitField("Save Category")

    
    def validate_name(self, name):
        category = BookCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError(f"This name {category.name} already exist as Category please use a different one")