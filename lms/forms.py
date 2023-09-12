from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (
    BooleanField,
    EmailField,
    FileField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerRangeField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)

import isbnlib

from lms.models import Author, Book, BookCategory, Librarian, Student

images = UploadSet("images", IMAGES)


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])


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
        author = Author.query.filter_by(name=name.data.lower()).first()
        existing_author = Author.query.filter_by(name=name.data.upper()).first()

        if author:
            raise ValidationError(
                f"This name {author.name} already exist as an Author please use a different one"
            )

        elif existing_author:
            raise ValidationError(
                f"This name {existing_author.name} already exist as an Author please use a different one"
            )


class BookCategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired()])
    submit = SubmitField("Save Category")

    def validate_name(self, name):
        category = BookCategory.query.filter_by(name=name.data.lower()).first()
        existing_category = BookCategory.query.filter_by(name=name.data.upper()).first()

        if category:
            raise ValidationError(
                f"This name {category.name} already exist as Category please use a different one"
            )
        elif existing_category:
            raise ValidationError(
                f"This name {existing_category.name} already exist as Category please use a different one"
            )


class BookForm(FlaskForm):
    book_category_id = SelectField("Category", validators=[DataRequired()])
    author_id = SelectField("Author", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    version = StringField(
        "Version",
        validators=[
            DataRequired(),
            Regexp(r"^v[1-2]$", message='Invalid version format. Use "v1" or "v2".'),
        ],
    )
    publisher = StringField("Publisher", validators=[DataRequired()])
    isbn = IntegerField("Isbn", validators=[DataRequired()])
    img_upload = FileField(
        "Image Upload", validators=[FileRequired(), FileAllowed(images, "Images only!")]
    )
    total_copies = IntegerRangeField("Total Copies", validators=[DataRequired()])

    submit = SubmitField("Save Book")

    def validate_isbn(self, isbn):
        if not isbnlib.is_isbn10(isbn.data) and not isbnlib.is_isbn13(isbn.data):
            raise ValidationError("Invalid ISBN number. Please provide a valid ISBN-10 or ISBN-13.")
        isbn = Book.query.filter_by(isbn=isbn.data).first()
        if isbn:
            raise ValidationError(
                f"This number {isbn.name} already exist as an isbn used to register another book please use a different one"
            )

