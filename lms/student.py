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


@student.route("/student/book", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def books():
    form = SearchForm()
    books = Book.query.order_by(Book.id.desc()).paginate(per_page=5, error_out=False)
    return render_template("student/books.html", books=books, form=form)


@student.route("/student/books/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def single_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        flash("Book not found.", "warning")
        return redirect(url_for("student.books"))
        
    return render_template("student/single_book.html", book=book)


@student.route("/student/issue_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def issue_book(book_id):
        book = Book.query.filter_by(id=book_id).first()

        single_book = Book.query.filter(Book.isbn == book.isbn, Book.available_copies > 0).first()
        student_id = Student.query.filter_by(matric_no=current_user.matric_no).first()
        if not  single_book:
            flash("Book is not available for issue", "danger")
            return render_template('student/single_book.html', book=book)
        single_book.available_copies-=1
        single_book , student_id= single_book.id, student_id.id
           
        issued_book = Issue(
            student_id=student_id,
            book_id=single_book,
        )
        issued_book.set_expiry_date(datetime.utcnow())
        db.session.add(issued_book)

        try:
            db.session.commit()
            flash("Book issued successfully", "success")
            return redirect(url_for("student.single_book", book_id=book_id))
        except Exception as e:
            flash(f"An error occurred while issuing a book: {str(e)}", "danger")
            return redirect(url_for("student.single_book", book_id=book_id))


@student.route("/student/reserve_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def reserve_book(book_id):
        book = Book.query.filter_by(id=book_id).first()

        single_book = Book.query.filter(Book.isbn == book.isbn, Book.available_copies > 0).first()
        student_id = Student.query.filter_by(matric_no=current_user.matric_no).first()
        if not  single_book:
            flash("Book is not available for reservation", "danger")
            return render_template('student/single_book.html', book=book)
        single_book , student_id= single_book.id, student_id.id
           
        reserve = Reservation(
            student_id=student_id,
            book_id=single_book,
            reservation_date=datetime.utcnow()
        )
        db.session.add(reserve)

        try:
            db.session.commit()
            flash("Book reserved successfully", "success")
            return redirect(url_for("student.single_book", book_id=book_id))
        except Exception as e:
            flash(f"An error occurred while processing reservation: {str(e)}", "danger")
            return redirect(url_for("student.single_book", book_id=book_id))
        
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
