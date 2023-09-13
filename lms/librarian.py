from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from lms.decorator import session_expired_handler
from lms.extensions import db
from lms.forms import AuthorForm, BookCategoryForm, BookForm, SearchForm
from lms.models import Author, Book, BookCategory
from lms.forms import images
from werkzeug.exceptions import RequestEntityTooLarge
from flask_uploads import UploadNotAllowed
from werkzeug.utils import secure_filename
import secrets

librarian = Blueprint(
    "librarian", __name__, template_folder="templates", static_folder="assets"
)


@librarian.route("/librarian/dashboard", methods=["GET", "POST"])
@session_expired_handler("librarian")
def dashboard():
    return render_template("librarian/dashboard.html")


""" Author section"""


@librarian.route("/librarian/author", methods=["GET", "POST"])
@session_expired_handler("librarian")
def author():
    form = SearchForm()
    author = Author.query.paginate(per_page=3, error_out=False)
    return render_template("librarian/author.html", author=author, form=form)


@librarian.route("/librarian/add_author", methods=["GET", "POST"])
@session_expired_handler("librarian")
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        name = form.name.data.lower().strip()
        author = Author(name=name)
        db.session.add(author)
        try:
            db.session.commit()
            flash("Author added successfully", "success")
            return redirect(url_for("librarian.author"))
        except Exception as e:
            flash(f"An error occurred while adding a new author: {str(e)}", "danger")
            return redirect(url_for("librarian.add_author"))
    return render_template("librarian/add_author.html", form=form)


@librarian.route("/librarian/edit_author/<int:author_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def edit_author(author_id):
    author = Author.query.get(author_id)
    if author is None:
        flash("Author not found", "danger")
        return redirect(url_for("librarian.author"))

    form = AuthorForm()
    if form.validate_on_submit():
        try:
            author.name = form.name.data.lower().strip()
            db.session.commit()
            flash("Author edited successfully", "success")
            return redirect(url_for("librarian.author"))
        except Exception as e:
            flash(f"An error occurred while editing Author details: {str(e)}", "danger")
            return redirect(url_for("librarian.add_author"))

    return render_template("librarian/edit_author.html", form=form, id=author.id)


@librarian.route("/librarian/remove_author/<int:author_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def remove_author(author_id):
    author = Author.query.get(author_id)
    db.session.delete(author)
    try:
        db.session.commit()
        flash(f"Author {author.name} Deleted successfully", "success")
        return redirect(url_for("librarian.author"))
    except Exception as e:
        flash(f"An error occurred while deleting Author details: {str(e)}", "danger")
    return redirect(url_for("librarian.author"))


""" Category section"""


@librarian.route("/librarian/category", methods=["GET", "POST"])
@session_expired_handler("librarian")
def category():
    form = SearchForm()
    category = BookCategory.query.paginate(per_page=3, error_out=False)
    return render_template("librarian/category.html", form=form, category=category)


@librarian.route("/librarian/add_category", methods=["GET", "POST"])
@session_expired_handler("librarian")
def add_category():
    form = BookCategoryForm()
    if form.validate_on_submit():
        name = form.name.data.lower().strip()
        category = BookCategory(name=name)
        db.session.add(category)
        try:
            db.session.commit()
            flash("Category added successfully", "success")
            return redirect(url_for("librarian.category"))
        except Exception as e:
            flash(f"An error occurred while adding a new Category: {str(e)}", "danger")
            return redirect(url_for("librarian.add_category"))
    return render_template("librarian/add_category.html", form=form)


@librarian.route("/librarian/edit_category/<int:category_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def edit_category(category_id):
    category = BookCategory.query.get(category_id)
    if category is None:
        flash("BookCategory not found", "danger")
        return redirect(url_for("librarian.categoryr"))

    form = BookCategoryForm()
    if form.validate_on_submit():
        try:
            category.name = form.name.data.lower().strip()
            db.session.commit()
            flash("BookCategory edited successfully", "success")
            return redirect(url_for("librarian.category"))
        except Exception as e:
            flash(
                f"An error occurred while editing BookCategory details: {str(e)}",
                "danger",
            )
            return redirect(url_for("librarian.add_category"))
    return render_template("librarian/edit_category.html", id=category.id, form=form)


@librarian.route(
    "/librarian/remove_category/<int:category_id>", methods=["GET", "POST"]
)
@session_expired_handler("librarian")
def remove_category(category_id):
    category = BookCategory.query.get(category_id)
    db.session.delete(category)
    try:
        db.session.commit()
        flash(f"Category {category.name} Deleted successfully", "success")
        return redirect(url_for("librarian.category"))
    except Exception as e:
        flash(f"An error occurred while deleting Category details: {str(e)}", "danger")
    return redirect(url_for("librarian.category"))


""" Book section"""


@librarian.route("/librarian/books", methods=["GET", "POST"])
@session_expired_handler("librarian")
def books():
    return render_template("librarian/books.html")


@librarian.route("/librarian/add_book", methods=["GET", "POST"])
@session_expired_handler("librarian")
def add_book():
    form = BookForm()
    categories = BookCategory.query.all()
    authors = Author.query.all()

    form.book_category_id.choices = [(str(category.id), category.name) for category in categories]
    form.author_id.choices = [(str(author.id), author.name) for author in authors]


    if form.validate_on_submit():
        book_category_id = form.book_category_id.data
        author_id = form.author_id.data
        title = form.title.data.lower().strip()
        description = form.description.data.strip()
        version = form.version.data
        publisher = form.publisher.data.lower().strip()
        isbn = form.isbn.data
        img_upload = form.img_upload.data
        total_copies = form.total_copies.data
        
 
        filename = secure_filename(img_upload.filename)
        img_ext = filename.split(".")[-1].lower()
        random_number = secrets.token_hex(16)
        random_filename = f"{random_number}.{img_ext}"
                
        images.save(img_upload, name=random_filename)
        
        print(book_category_id)
        print(author_id)
        print(title)
        print(description)
        print(version)
        print(publisher)
        print(isbn)
        print(img_upload)
        print(total_copies)

        # book = Book(
        #     book_category_id=book_category_id,
        #     author_id=author_id,
        #     title=title,
        #     description=description,
        #     version=version,
        #     publisher=publisher,
        #     isbn=isbn,
        #     img_upload=img_upload,
        #     total_copies=total_copies,
        # )
        # db.session.add(book)
        # try:
        #     db.session.commit()
        #     flash("Book added successfully", "success")
        #     return redirect(url_for("librarian.book"))
        # except Exception as e:
        #     flash(f"An error occurred while adding a new book: {str(e)}", "danger")
        #     return redirect(url_for("librarian.add_book"))
    return render_template("librarian/add_book.html", form=form)


@librarian.route("/librarian/edit_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def edit_book(book_id):
    return render_template("librarian/edit_book.html")


@librarian.route("/librarian/remove_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def remove_book(book_id):
    return redirect(url_for("librarian.books"))


""" Student section"""


@librarian.route("/librarian/students", methods=["GET", "POST"])
@session_expired_handler("librarian")
def students():
    return render_template("librarian/students.html")


@librarian.route("/librarian/add_student", methods=["GET", "POST"])
@session_expired_handler("librarian")
def add_student():
    return render_template("librarian/add_student.html")


@librarian.route("/librarian/edit_student/<int:student_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def edit_student(student_id):
    return render_template("librarian/edit_student.html")


@librarian.route("/librarian/remove_student/<int:student_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
def remove_student(student_id):
    return render_template("librarian/remove_student.html")


""" Issue section"""


@librarian.route("/librarian/issued_book", methods=["GET", "POST"])
@session_expired_handler("librarian")
def issued_book():
    return render_template("librarian/issued_book.html")


""" search section"""


@librarian.route(f"/librarian/author/searchq=", methods=["GET", "POST"])
@session_expired_handler("librarian")
def search_author():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data.lower().split()
        author = Author.query.filter(Author.name.ilike(f"%{query}%")).paginate(
            per_page=3, error_out=False
        )
    return render_template("librarian/author.html", form=form, author=author)


""" search section"""


@librarian.route(f"/librarian/category/searchq=", methods=["GET", "POST"])
@session_expired_handler("librarian")
def search_category():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        category = BookCategory.query.filter(
            BookCategory.name.ilike(f"%{query}%")
        ).paginate(per_page=3, error_out=False)
    return render_template("librarian/category.html", form=form, category=category)
