from flask import Blueprint, url_for
from flask import render_template, redirect
from flask_login import login_required

student = Blueprint("student", __name__, template_folder="templates", static_folder="assets")

@student.route('/student/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('student/dashboard.html')

@student.route('/student/books', methods=["GET", "POST"])
@login_required
def books():
    return render_template('student/books.html')

@student.route('/student/books/<int:book_id>', methods=["GET", "POST"])
@login_required
def single_book(book_id):
    return render_template('student/single_book.html')

@student.route('/student/request_book', methods=["GET", "POST"])
@login_required
def request_book():
    return redirect(url_for('student.single_book'))

@student.route('/student/profile', methods=["GET", "POST"])
@login_required
def profile():
    return render_template('student/profile.html')

@student.route('/student/fine', methods=["GET", "POST"])
@login_required
def fine():
    return render_template('student/fine.html')

@student.route('/student/payment', methods=["GET", "POST"])
@login_required
def payment():
    return render_template('student/payment.html')

@student.route('/student/payment_status', methods=["GET", "POST"])
@login_required
def payment_status():
    return render_template('student/payment_status.html')
