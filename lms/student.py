from flask import Blueprint, url_for
from flask import render_template, redirect
from flask_login import login_required
from lms.decorator import session_expired_handler

student = Blueprint("student", __name__, template_folder="templates", static_folder="assets")

@student.route('/student/dashboard', methods=["GET", "POST"])
@session_expired_handler('student')
def dashboard():
    return render_template('student/dashboard.html')

@student.route('/student/books', methods=["GET", "POST"])
@session_expired_handler('student')
def books():
    return render_template('student/books.html')

@student.route('/student/books/<int:book_id>', methods=["GET", "POST"])
@session_expired_handler('student')
def single_book(book_id):
    return render_template('student/single_book.html')

@student.route('/student/request_book', methods=["GET", "POST"])
@session_expired_handler('student')
def request_book():
    return redirect(url_for('student.single_book'))

@student.route('/student/profile', methods=["GET", "POST"])
@session_expired_handler('student')
def profile():
    return render_template('student/profile.html')

@student.route('/student/fine', methods=["GET", "POST"])
@session_expired_handler('student')
def fine():
    return render_template('student/fine.html')

@student.route('/student/payment', methods=["GET", "POST"])
@session_expired_handler('student')
def payment():
    return render_template('student/payment.html')

@student.route('/student/payment_status', methods=["GET", "POST"])
@session_expired_handler('student')
def payment_status():
    return render_template('student/payment_status.html')
