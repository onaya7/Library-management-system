import secrets

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user
from werkzeug.utils import secure_filename

from lms.decorator import role_required, session_expired_handler
from lms.extensions import db
from lms.forms import (
    AuthorForm,
    BookCategoryForm,
    BookForm,
    EditBookForm,
    EditStudentForm,
    SearchForm,
    StudentForm,
    images,
)
from lms.models import Author, Book, BookCategory, Student

librarian = Blueprint(
    "librarian", __name__, template_folder="templates", static_folder="assets"
)


@librarian.route("/librarian/dashboard", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def dashboard():
    cookie = request.cookies.get("token", "")
    # how to decrypt this cookie and see it values

    return render_template("librarian/dashboard.html")


""" Author section"""


@librarian.route("/librarian/author", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def author():
    form = SearchForm()

    author = Author.query.order_by(Author.name).paginate(per_page=5, error_out=False)

    return render_template("librarian/author.html", author=author, form=form)


""" search section"""


@librarian.route(f"/librarian/author/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_author():
    form = SearchForm()
    author = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        author = Author.query.filter(Author.name.ilike(f"%{query}%")).paginate(
            per_page=5, error_out=False
        )

    return render_template("librarian/author.html", form=form, author=author)


@librarian.route("/librarian/add_author", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
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
@role_required("librarian")
def edit_author(author_id):
    author = Author.query.get(author_id)
    if author is None:
        flash("Author not found", "danger")
        return redirect(url_for("librarian.author"))

    form = AuthorForm(obj=author)
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
@role_required("librarian")
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
@role_required("librarian")
def category():
    form = SearchForm()
    category = BookCategory.query.order_by(BookCategory.name).paginate(
        per_page=5, error_out=False
    )
    return render_template("librarian/category.html", form=form, category=category)


""" search section"""


@librarian.route(f"/librarian/category/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_category():
    form = SearchForm()
    category = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        category = BookCategory.query.filter(
            BookCategory.name.ilike(f"%{query}%")
        ).paginate(per_page=5, error_out=False)
    return render_template("librarian/category.html", form=form, category=category)


@librarian.route("/librarian/add_category", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
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
@role_required("librarian")
def edit_category(category_id):
    category = BookCategory.query.get(category_id)
    if category is None:
        flash("BookCategory not found", "danger")
        return redirect(url_for("librarian.category"))

    form = BookCategoryForm(obj=category)
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
@role_required("librarian")
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
@role_required("librarian")
def books():
    form = SearchForm()
    books = Book.query.order_by(Book.title).paginate(per_page=5, error_out=False)
    return render_template("librarian/books.html", books=books, form=form)


""" search section"""


@librarian.route("/librarian/books/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_books():
    form = SearchForm()
    books = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        books = Book.query.filter(Book.isbn.ilike(f"%{query}%")).paginate(
            per_page=5, error_out=False
        )

    return render_template("librarian/books.html", form=form, books=books)


@librarian.route("/librarian/add_book", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def add_book():
    form = BookForm()
    categories = BookCategory.query.order_by(BookCategory.name).all()
    authors = Author.query.order_by(Author.name).all()

    form.book_category_id.choices = [
        (str(category.id), category.name) for category in categories
    ]
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
        random_number = secrets.token_hex(10)
        random_filename = f"{random_number}.{img_ext}"

        images.save(img_upload, name=random_filename)

        book = Book(
            book_category_id=book_category_id,
            author_id=author_id,
            title=title,
            description=description,
            version=version,
            publisher=publisher,
            isbn=isbn,
            img_upload=random_filename,
            total_copies=total_copies,
        )
        db.session.add(book)
        try:
            db.session.commit()
            flash("Book added successfully", "success")
            return redirect(url_for("librarian.books"))
        except Exception as e:
            flash(f"An error occurred while adding a new book: {str(e)}", "danger")
            return redirect(url_for("librarian.add_book"))
    return render_template("librarian/add_book.html", form=form)


@librarian.route("/librarian/edit_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = EditBookForm(obj=book)
    categories = BookCategory.query.order_by(BookCategory.name).all()
    authors = Author.query.order_by(Author.name).all()

    form.book_category_id.choices = [
        (str(category.id), category.name) for category in categories
    ]
    form.author_id.choices = [(str(author.id), author.name) for author in authors]

    if form.validate_on_submit():
        book_category_id = form.book_category_id.data
        author_id = form.author_id.data
        title = form.title.data.lower().strip()
        description = form.description.data.strip()
        version = form.version.data
        publisher = form.publisher.data.lower().strip()
        isbn = form.isbn.data
        total_copies = form.total_copies.data

        # Handle image upload if a new image is provided
        img_upload = form.img_upload.data
        if img_upload:
            filename = secure_filename(img_upload.filename)
            img_ext = filename.split(".")[-1].lower()
            random_number = secrets.token_hex(10)
            random_filename = f"{random_number}.{img_ext}"
            images.save(img_upload, name=random_filename)

        book.edit_book_details(
            book_category_id=book_category_id,
            author_id=author_id,
            title=title,
            description=description,
            version=version,
            publisher=publisher,
            isbn=isbn,
            img_upload=random_filename,
            total_copies=total_copies,
        )

        try:
            db.session.commit()
            flash("Book updated successfully", "success")
            return redirect(url_for("librarian.books"))
        except Exception as e:
            flash(f"An error occurred while updating the book: {str(e)}", "danger")
            return redirect(url_for("librarian.edit_book", book_id=book.id))

    return render_template("librarian/edit_book.html", form=form, book=book)


@librarian.route("/librarian/remove_book/<int:book_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def remove_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book removed successfully", "success")
        return redirect(url_for("librarian.books"))
    except Exception as e:
        flash(f"An error occurred while removing the book: {str(e)}", "danger")
        return redirect(url_for("librarian.books"))


""" Student section"""


@librarian.route("/librarian/students", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def students():
    form = SearchForm()
    student = Student.query.order_by(Student.name).paginate(per_page=5, error_out=False)
    return render_template("librarian/students.html", student=student, form=form)


"""student search section"""


@librarian.route("/librarian/students/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_students():
    form = SearchForm()
    student = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        student = Student.query.filter(Student.matric_no.ilike(f"%{query}%")).paginate(
            per_page=10, error_out=False
        )
    return render_template("librarian/students.html", form=form, student=student)


@librarian.route("/librarian/add_student", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def add_student():
    form = StudentForm()

    if form.validate_on_submit():
        name = form.name.data.lower().strip()
        password = form.password.data
        matric_no = form.matric_no.data
        department = form.department.data.lower().strip()
        email = form.email.data.lower().strip()
        img_upload = form.img_upload.data
        student_status = form.student_status.data

        filename = secure_filename(img_upload.filename)
        img_ext = filename.split(".")[-1].lower()
        random_number = secrets.token_hex(10)
        random_filename = f"{random_number}.{img_ext}"
        images.save(img_upload, name=random_filename)

        student = Student(
            name=name,
            password=password,
            matric_no=matric_no,
            department=department,
            email=email,
            img_upload=random_filename,
            student_status=student_status,
        )
        student.generate_password_hash(password)
        db.session.add(student)
        try:
            db.session.commit()
            flash("Student added successfully", "success")
            return redirect(url_for("librarian.students"))
        except Exception as e:
            flash(f"An error occurred while adding a new student: {str(e)}", "danger")
            return redirect(url_for("librarian.add_student"))

    return render_template("librarian/add_student.html", form=form)


@librarian.route("/librarian/edit_student/<int:student_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = EditStudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data.lower().strip()
        student.matric_no = form.matric_no.data
        student.department = form.department.data.lower().strip()
        student.email = form.email.data.lower().strip()
        student.student_status = form.student_status.data
        # Handle image upload if a new image is provided
        img_upload = form.img_upload.data
        if img_upload:
            filename = secure_filename(img_upload.filename)
            img_ext = filename.split(".")[-1].lower()
            random_number = secrets.token_hex(10)
            random_filename = f"{random_number}.{img_ext}"
            images.save(img_upload, name=random_filename)
        student.img_upload = random_filename
        try:
            db.session.commit()
            flash("Student updated successfully", "success")
            return redirect(url_for("librarian.students"))
        except Exception as e:
            flash(f"An error occurred while updating the student: {str(e)}", "danger")
            return redirect(url_for("librarian.edit_student", student_id=student.id))
    return render_template("librarian/edit_student.html", form=form, student=student)


@librarian.route("/librarian/remove_student/<int:student_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def remove_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student removed successfully", "success")
        return redirect(url_for("librarian.students"))
    except Exception as e:
        flash(f"An error occurred while removing the student: {str(e)}", "danger")
        return redirect(url_for("librarian.students"))


""" Issue section"""


@librarian.route("/librarian/issued_book", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def issued_book():
    return render_template("librarian/issued_book.html")


@librarian.route("/upload/<path:filename>")
@session_expired_handler("librarian")
def upload(filename):
    return send_from_directory(
        current_app.config["UPLOADED_IMAGES_DEST"], filename, as_attachment=True
    )
