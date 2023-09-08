from flask import render_template, redirect, url_for
from flask import Blueprint
from lms.decorator import session_expired_handler

librarian = Blueprint("librarian", __name__, template_folder="templates", static_folder="assets")

@librarian.route('/librarian/dashboard', methods=["GET", "POST"])
@session_expired_handler('librarian')
def dashboard():
    return render_template('librarian/dashboard.html')

""" Author section"""
@librarian.route('/librarian/author', methods=["GET", "POST"])
@session_expired_handler('librarian')
def author():
    return render_template('librarian/author.html')
@librarian.route('/librarian/add_author', methods=["GET", "POST"])
@session_expired_handler('librarian')
def add_author():
    return render_template('librarian/add_author.html')

@librarian.route('/librarian/edit_author/<int:author_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def edit_author(author_id):
    return render_template('librarian/edit_author.html')

@librarian.route('/librarian/remove_author/<int:author_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def remove_author(author_id):
    return render_template('librarian/remove_author.html')


""" Category section"""
@librarian.route('/librarian/category', methods=["GET", "POST"])
@session_expired_handler('librarian')
def category():
    return render_template('librarian/category.html')
@librarian.route('/librarian/add_category', methods=["GET", "POST"])
@session_expired_handler('librarian')
def add_category():
    return render_template('librarian/add_category.html')

@librarian.route('/librarian/edit_category/<int:category_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def edit_category(category_id):
    return render_template('librarian/edit_category.html')

@librarian.route('/librarian/remove_category/<int:category_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def remove_category(category_id):
    return render_template('librarian/remove_category.html')

""" Book section"""
@librarian.route('/librarian/books', methods=["GET", "POST"])
@session_expired_handler('librarian')
def books():
    return render_template('librarian/books.html')

@librarian.route('/librarian/add_book', methods=["GET", "POST"])
@session_expired_handler('librarian')
def add_book():
    return render_template('librarian/add_book.html')

@librarian.route('/librarian/edit_book/<int:book_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def edit_book(book_id):
    return render_template('librarian/edit_book.html')

@librarian.route('/librarian/remove_book/<int:book_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def remove_book(book_id):
    return redirect(url_for('librarian.books'))

""" Student section"""
@librarian.route('/librarian/students', methods=["GET", "POST"])
@session_expired_handler('librarian')
def students():
    return render_template('librarian/students.html')
@librarian.route('/librarian/add_student', methods=["GET", "POST"])
@session_expired_handler('librarian')
def add_student():
    return render_template('librarian/add_student.html')

@librarian.route('/librarian/edit_student/<int:student_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def edit_student(student_id):
    return render_template('librarian/edit_student.html')

@librarian.route('/librarian/remove_student/<int:student_id>', methods=["GET", "POST"])
@session_expired_handler('librarian')
def remove_student(student_id):
    return render_template('librarian/remove_student.html')

""" Issue section"""
@librarian.route('/librarian/issued_book', methods=["GET", "POST"])
@session_expired_handler('librarian')
def issued_book():
    return render_template('librarian/issued_book.html')




