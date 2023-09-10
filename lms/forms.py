from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)

from lms.models import Author, BookCategory, Librarian, Student


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
            raise ValidationError(
                f"This name {author.name} already exist as an Author please use a different one"
            )


class BookCategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired()])
    submit = SubmitField("Save Category")

    def validate_name(self, name):
        category = BookCategory.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError(
                f"This name {category.name} already exist as Category please use a different one"
            )


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
