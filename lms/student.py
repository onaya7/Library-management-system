from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from lms.decorator import role_required, session_expired_handler
from lms.models import *
from lms.forms import SearchForm

student = Blueprint(
    "student", __name__, template_folder="templates", static_folder="assets"
)


@student.route("/student/dashboard", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def dashboard():
    book = Book.query.order_by(Book.id.desc()).paginate(per_page=5, error_out=False)
    category = BookCategory.query.order_by(BookCategory.id.desc()).paginate(per_page=5, error_out=False)
    issue = Issue.query.filter_by(student_id=current_user.id).order_by(Issue.issued_date.desc()).paginate(per_page=5, error_out=False)
    reserve = Reservation.query.filter_by(student_id=current_user.id).order_by(Reservation.reservation_date.desc()).paginate(per_page=5, error_out=False)
    fine = Fine.query.filter_by(student_id=current_user.id, status=False).order_by(Fine.id.desc()).paginate(per_page=5, error_out=False)

    return render_template("student/dashboard.html", book=book, fine=fine, category=category, reserve=reserve, issue=issue)

""" search section"""
@student.route("/student/book/search", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def search_book():
    form = SearchForm()
    books = None
    if form.validate_on_submit():
            query = form.query.data.lower().strip()

            # Perform case-insensitive search on both title and ISBN
            books = Book.query.filter(
                db.or_(Book.title.ilike(f"%{query}%"), Book.isbn.ilike(f"%{query}%"))
            ).paginate(per_page=5, error_out=False)

            if not books.items:
                flash("No books found with the given title or ISBN.", "info")
            elif books.total == 0:
                flash("No results found.", "info")
    return render_template("student/books.html", form=form, books=books)


@student.route("/student/books", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def books():
    form = SearchForm()
    books = Book.query.order_by(Book.id.desc()).paginate(per_page=5, error_out=False)
    return render_template("student/books.html", books=books, form=form)


@student.route("/student/books/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
def single_book(book_id):
    return render_template("student/single_book.html")


@student.route("/student/request_book", methods=["GET", "POST"])
@session_expired_handler("student")
def request_book():
    return redirect(url_for("student.single_book"))


@student.route("/student/profile", methods=["GET", "POST"])
@session_expired_handler("student")
def profile():
    return render_template("student/profile.html")


@student.route("/student/fine", methods=["GET", "POST"])
@session_expired_handler("student")
def fine():
    return render_template("student/fine.html")


@student.route("/student/payment", methods=["GET", "POST"])
@session_expired_handler("student")
def payment():
    return render_template("student/payment.html")


@student.route("/student/payment_status", methods=["GET", "POST"])
@session_expired_handler("student")
def payment_status():
    return render_template("student/payment_status.html")
