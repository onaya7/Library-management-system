import requests
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from lms.config import Config
from lms.decorator import role_required, session_expired_handler
from lms.forms import SearchForm
from lms.helpers import generate_transaction_id
from lms.models import *

student = Blueprint(
    "student", __name__, template_folder="templates", static_folder="assets"
)


@student.route("/student/dashboard", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def dashboard():
    book = Book.query.order_by(Book.id.desc()).paginate(per_page=3, error_out=False)
    category = BookCategory.query.order_by(BookCategory.id.desc()).paginate(
        per_page=5, error_out=False
    )
    issue = (
        Issue.query.filter_by(student_id=current_user.id)
        .order_by(Issue.issued_date.desc())
        .paginate(per_page=5, error_out=False)
    )

    payment = (
        Payment.query.filter_by(student_id=current_user.id)
        .order_by(Payment.payment_date.desc())
        .paginate(per_page=5, error_out=False)
    )
    reserve = (
        Reservation.query.filter_by(student_id=current_user.id)
        .order_by(Reservation.reservation_date.desc())
        .paginate(per_page=5, error_out=False)
    )
    fine = (
        Fine.query.filter_by(student_id=current_user.id, status=False)
        .order_by(Fine.id.desc())
        .paginate(per_page=5, error_out=False)
    )

    return render_template(
        "student/dashboard.html",
        book=book,
        fine=fine,
        category=category,
        reserve=reserve,
        issue=issue,
        payment=payment,
    )


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


"""issued book search section"""


@student.route("/student/issued_book/search", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def search_issue():
    form = SearchForm()
    issue = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        try:
            # Convert the user input into a valid date
            issued_date = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "warning")
            return render_template("student/issue_history.html", form=form, issue=issue)

        issue = Issue.query.filter(Issue.issued_date == issued_date).paginate(
            per_page=10, error_out=False
        )

        if not issue.items:
            flash("No issue found with the given issued date.", "info")
        elif issue.total == 0:
            flash("No results found.", "info")
    return render_template("student/issue_history.html", form=form, issue=issue)


@student.route("/student/issue_history", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def issue_history():
    form = SearchForm()
    issue = (
        Issue.query.filter_by(student_id=current_user.id)
        .order_by(Issue.issued_date.desc())
        .paginate(per_page=5, error_out=False)
    )
    return render_template("student/issue_history.html", issue=issue, form=form)


@student.route("/student/issue_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def issue_book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    single_book = Book.query.filter(
        Book.isbn == book.isbn, Book.available_copies > 0
    ).first()
    student_id = Student.query.filter_by(matric_no=current_user.matric_no).first()
    if not single_book:
        flash("Book is not available for issue", "danger")
        return render_template("student/single_book.html", book=book)
    single_book.available_copies -= 1
    single_book, student_id = single_book.id, student_id.id

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


"""reserve book search section"""


@student.route("/student/reserve_book/search", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def search_reserve():
    form = SearchForm()
    reserve = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        try:
            # Convert the user input into a valid date
            reservation_date = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "warning")
            return render_template(
                "student/reserve_history.html", form=form, reserve=reserve
            )

        reserve = Reservation.query.filter(
            Reservation.reservation_date == reservation_date
        ).paginate(per_page=10, error_out=False)
        if not reserve.items:
            flash("No reserve found with the given reservation date.", "info")
        elif reserve.total == 0:
            flash("No results found.", "info")
    return render_template("student/reserve_history.html", form=form, reserve=reserve)


@student.route("/student/reserve_history", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def reserve_history():
    form = SearchForm()
    reserve = (
        Reservation.query.filter_by(student_id=current_user.id)
        .order_by(Reservation.reservation_date)
        .paginate(per_page=5, error_out=False)
    )
    return render_template("student/reserve_history.html", reserve=reserve, form=form)


@student.route("/student/reserve_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def reserve_book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    single_book = Book.query.filter(
        Book.isbn == book.isbn, Book.available_copies > 0
    ).first()
    student_id = Student.query.filter_by(matric_no=current_user.matric_no).first()
    if not single_book:
        flash("Book is not available for reservation", "danger")
        return render_template("student/single_book.html", book=book)
    single_book, student_id = single_book.id, student_id.id

    reserve = Reservation(
        student_id=student_id, book_id=single_book, reservation_date=datetime.utcnow()
    )
    db.session.add(reserve)

    try:
        db.session.commit()
        flash("Book reserved successfully", "success")
        return redirect(url_for("student.single_book", book_id=book_id))
    except Exception as e:
        flash(f"An error occurred while processing reservation: {str(e)}", "danger")
        return redirect(url_for("student.single_book", book_id=book_id))


""" Fine section"""


@student.route("/student/fine", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def fine():
    form = SearchForm()
    fine = (
        Fine.query.filter_by(student_id=current_user.id)
        .order_by(Fine.student_id)
        .paginate(per_page=5, error_out=False)
    )
    return render_template("student/fine.html", fine=fine, form=form)


"""Fine  search section"""


@student.route("/student/fine/search", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def search_fine():
    form = SearchForm()
    fine = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        fine = Fine.query.filter(
            Fine.student_id == current_user.id, Fine.matric_no.ilike(f"%{query}%")
        ).paginate(per_page=10, error_out=False)
        if not fine.items:
            flash("No fine found with the given matric number.", "info")
        elif fine.total == 0:
            flash("No results found.", "info")
    return render_template("student/fine.html", form=form, fine=fine)


""" Transaction section"""


@student.route("/student/transaction", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def transaction():
    form = SearchForm()
    payment = (
        Payment.query.filter_by(student_id=current_user.id)
        .order_by(Payment.payment_date.desc())
        .paginate(per_page=5, error_out=False)
    )
    return render_template("student/transaction.html", payment=payment, form=form)


""" search section"""


@student.route("/student/transaction/search", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def search_transaction():
    form = SearchForm()
    payment = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        payment = Payment.query.filter(
            Payment.student_id == current_user.id,
            Payment.payment_date.ilike(f"%{query}%"),
        ).paginate(per_page=10, error_out=False)
        if not payment.items:
            flash(
                "No payment found with the given transaction date. try 2023-10-24",
                "info",
            )
        elif payment.total == 0:
            flash("No results found.", "info")

    return render_template("student/transaction.html", form=form, payment=payment)


@student.route("/student/profile", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def profile():
    student = Student.query.filter_by(matric_no=current_user.matric_no).first()
    if student is None:
        flash("Student not found.", "warning")
        return redirect(url_for("student.profile"))
    return render_template("student/profile.html")


"""Fine  payment section"""


@student.route("/student/fine/payment/<int:fine_id>", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def fine_payment(fine_id):
    fine = Fine.query.get_or_404(fine_id)

    try:
        flw_secret_key = Config.FLW_SECRET_KEY
        url = "https://api.flutterwave.com/v3/payments"
        headers = {
            "Authorization": f"Bearer {flw_secret_key}",
            "Content-Type": "application/json",
        }
        # Generate a unique transaction reference
        tx_ref = generate_transaction_id()
        payload = {
            "tx_ref": tx_ref,
            "amount": fine.amount,
            "currency": "NGN",
            "redirect_url": "https://lms.devonaya.com/student/fine/payment_status",
            "meta": {
                "student_id": current_user.alternative_id,
                "student_name": current_user.name,
                "student_email": current_user.email,
                "matric_no": current_user.matric_no,
                "fine_id": fine.id,
                "fine_amount": fine.amount,
            },
            "customer": {
                "email": current_user.email,
                "name": current_user.name,
            },
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            payment_link = response.json().get("data", {}).get("link")
            return redirect(payment_link)
        else:
            flash(
                f"Payment request failed with status code: {response.status_code}",
                "danger",
            )
    except Exception as e:
        flash(f"An error occurred while processing payment: {str(e)}", "danger")
    return redirect(url_for("student.fine"))


@student.route("/student/fine/webhook/", methods=["POST"])
def fine_webhook():
    secret_hash = Config.FLW_SECRET_HASH
    signature = request.headers.get("Verif-Hash")
    if not signature or signature != secret_hash:
        return jsonify(status=401)
    payload = request.get_json()
    transaction_id = payload["data"]["id"]
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    flw_secret_key = Config.FLW_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {flw_secret_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(url=url, headers=headers)
    data = response.json()
    transaction_id = data["data"]["id"]
    existing_event = Payment.query.filter_by(transaction_id=data["data"]["id"]).first()
    if existing_event:
        existing_event_status = existing_event.status
        if existing_event_status == payload["data"]["status"]:
            print(existing_event_status == payload["data"]["status"])
            return jsonify(status=200)
        # The webhook status hasnt changed duplicate transaction
        else:
            fine_id = data["data"]["meta"]["fine_id"]
            fine = Fine.query.get(fine_id)
            if (
                payload["event"] == "charge.completed"
                and payload["data"]["status"] == "successful"
            ):
                fine.status = True
                existing_event.status = payload["data"]["status"]
                db.session.commit()
            else:
                fine.status = False
                existing_event.status = payload["data"]["status"]
            return jsonify(status=200)
    return jsonify(status=200)


@student.route("/student/fine/payment_status", methods=["GET", "POST"])
@session_expired_handler("student")
@role_required("student")
def fine_payment_status():
    try:
        data = request.args
        if data["status"] == "successful":
            transaction_id = data["transaction_id"]
            url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            flw_secret_key = Config.FLW_SECRET_KEY
            headers = {
                "Authorization": f"Bearer {flw_secret_key}",
                "Content-Type": "application/json",
            }
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                flash(
                    f"Hello an Error occurred during payment status processing: {str(e)}",
                    "danger",
                )
            data = response.json()
            fine_id = data["data"]["meta"]["fine_id"]
            fine = Fine.query.get(fine_id)
            if not fine:
                flash("No fine found for the current user", "danger")
            if (
                data["data"]["status"] == "successful"
                and data["data"]["amount"] == fine.amount
                and data["data"]["currency"] == "NGN"
            ):
                try:
                    fine.status = True
                    payment = Payment(
                        student_id=fine.student_id,
                        issue_id=fine.issue[0].id,
                        transaction_id=data["data"]["id"],
                        transaction_ref=data["data"]["tx_ref"],
                        amount=data["data"]["amount"],
                        status=data["data"]["status"],
                    )
                    db.session.add(payment)
                    db.session.commit()
                except Exception as e:
                    flash(
                        f"Please an Error occurred during payment status processing: {str(e)}",
                        "danger",
                    )
                    return redirect(url_for("student.fine"))
                flash("Payment successful", "success")
            else:
                flash("Payment failed", "danger")
            return redirect(url_for("student.fine"))
        else:
            flash("Payment failed", "danger")
            return redirect(url_for("student.fine"))
    except Exception as e:
        flash(f"An error occurred during payment status processing: {str(e)}", "danger")
        return redirect(url_for("student.fine"))


@student.route(
    "/student/fine/resend_webhook/<int:transaction_id>", methods=["GET", "POST"]
)
def resend_webhook(transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/resend-hook"
    flw_secret_key = Config.FLW_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {flw_secret_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url=url, headers=headers)
    data = response.json()
    print(data)
    flash("webhook sent successfully", "success")
    return redirect(url_for("student.fine"))
