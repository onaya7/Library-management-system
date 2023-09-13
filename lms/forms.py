import isbnlib
from flask_uploads import IMAGES, UploadSet, configure_uploads, UploadNotAllowed
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (BooleanField, EmailField, FileField, IntegerField,
                     IntegerRangeField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from lms.models import Author, Book, BookCategory, Librarian, Student
import os


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
    description = TextAreaField("Description", validators=[DataRequired()])
    version = StringField(
            "Version",
            validators=[
                DataRequired(),
                Regexp(r'^v\d+$', message='Invalid version format. Use "v" followed by a number, e.g., "v1".'),
            ],
        )
    publisher = StringField("Publisher", validators=[DataRequired()])
    isbn = IntegerField("Isbn", validators=[DataRequired()])
    img_upload = FileField(
            "Image Upload", validators=[
                FileRequired(message="Please select a file."),
                
            ]
        )
    total_copies = IntegerField("Total Copies", validators=[DataRequired()])

    submit = SubmitField("Save Book")

    def validate_isbn(self, isbn):
        isbn_str = str(isbn.data)  # Convert ISBN to a string
        if not isbnlib.is_isbn10(isbn_str) and not isbnlib.is_isbn13(isbn_str):
            raise ValidationError("Invalid ISBN number. Please provide a valid ISBN-10 or ISBN-13.")
        isbn = Book.query.filter_by(isbn=isbn.data).first()
        if isbn:
            raise ValidationError(
                f"This number {isbn.name} already exist as an isbn used to register another book please use a different one"
            )

    
    def validate_img_upload(self, img_upload):
        img_ext = img_upload.data.filename.split(".")[-1].lower()
        if img_ext not in ["jpg", "jpeg", "png", "mp4"]:
            raise ValidationError("Invalid image format. Please use a jpg, jpeg or png image.")

        default_size = 10 * 1024 * 1024  # 10MB
        img_upload.data.seek(0, os.SEEK_END)
        img_size = img_upload.data.tell()
        img_upload.data.seek(0)

        if img_size > default_size:
            raise ValidationError("Invalid image size. Please use an image smaller than 10MB.")

                
    

            
                
            
        

            
          


