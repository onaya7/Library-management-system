from flask import render_template, redirect, url_for
from flask import Blueprint
from flask_login import login_required

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="assets")

@librarian.route('/librarian/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('librarian/dashboard.html')

""" Category section"""
@librarian.route('/librarian/category', methods=["GET", "POST"])
@login_required
def category():
    return render_template('librarian/category.html')
@librarian.route('/librarian/add_category', methods=["GET", "POST"])
@login_required
def add_category():
    return render_template('librarian/add_category.html')

@librarian.route('/librarian/edit_category/<int:category_id>', methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    return render_template('librarian/edit_category.html')

@librarian.route('/librarian/remove_category/<int:category_id>', methods=["GET", "POST"])
@login_required
def remove_category(category_id):
    return render_template('librarian/remove_category.html')

""" Book section"""
@librarian.route('/librarian/books', methods=["GET", "POST"])
@login_required
def books():
    return render_template('librarian/books.html')

@librarian.route('/librarian/add_book', methods=["GET", "POST"])
@login_required
def add_book():
    return render_template('librarian/add_book.html')

@librarian.route('/librarian/edit_book/<int:book_id>', methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    return render_template('librarian/edit_book.html')

@librarian.route('/librarian/remove_book/<int:book_id>', methods=["GET", "POST"])
@login_required
def remove_book(book_id):
    return redirect(url_for('librarian.books'))

""" Student section"""
@librarian.route('/librarian/students', methods=["GET", "POST"])
@login_required
def students():
    return render_template('librarian/students.html')
@librarian.route('/librarian/add_student', methods=["GET", "POST"])
@login_required
def add_student():
    return render_template('librarian/add_student.html')

@librarian.route('/librarian/edit_student/<int:student_id>', methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    return render_template('librarian/edit_student.html')

@librarian.route('/librarian/remove_student/<int:student_id>', methods=["GET", "POST"])
@login_required
def remove_student(student_id):
    return render_template('librarian/remove_student.html')

""" Issue section"""
@librarian.route('/librarian/issued_book', methods=["GET", "POST"])
@login_required
def issued_book():
    return render_template('librarian/issued_book.html')




