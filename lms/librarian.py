import secrets
from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
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
    IssueBookForm,
    SearchForm,
    StudentForm,
    images,
)
from lms.helpers import calculate_fine, generate_library_card
from lms.models import (
    Author,
    Book,
    BookCategory,
    Fine,
    Issue,
    Librarian,
    LibraryCard,
    Payment,
    Reservation,
    Student,
)

librarian = Blueprint(
    "librarian", __name__, template_folder="templates", static_folder="assets"
)


@librarian.route("/librarian/dashboard", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def dashboard():
    author = Author.query.order_by(Author.name).paginate(per_page=5, error_out=False)
    book = Book.query.order_by(Book.id.desc()).paginate(per_page=3, error_out=False)
    student = Student.query.order_by(Student.id.desc()).paginate(
        per_page=5, error_out=False
    )
    category = BookCategory.query.order_by(BookCategory.name).paginate(
        per_page=5, error_out=False
    )
    issue = Issue.query.order_by(Issue.issued_date.desc()).paginate(
        per_page=5, error_out=False
    )
    fine = (
        Fine.query.filter(Fine.status == False)
        .order_by(Fine.id.desc())
        .paginate(per_page=5, error_out=False)
    )

    payment = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        per_page=5, error_out=False
    )
    reservation = Reservation.query.order_by(
        Reservation.reservation_date.desc()
    ).paginate(per_page=4, error_out=False)

    return render_template(
        "librarian/dashboard.html",
        author=author,
        category=category,
        book=book,
        student=student,
        issue=issue,
        fine=fine,
        reservation=reservation,
        payment=payment,
    )


""" Profile section """


@librarian.route("/librarian/profile", methods=["GET", "POST"])
@session_expired_handler("librarian")
def profile():
    librarian = Librarian.query.filter_by(id=current_user.id).first()
    if librarian is None:
        flash("librarian not found.", "warning")
        return redirect(url_for("librarian.profile"))
    return render_template("librarian/profile.html")


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

        if not author.items:
            flash("No author found with the given name.", "info")
        elif author.total == 0:
            flash("No results found.", "info")

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
        # Perform case-insensitive search on both title and ISBN
        books = Book.query.filter(
            db.or_(Book.title.ilike(f"%{query}%"), Book.isbn.ilike(f"%{query}%"))
        ).paginate(per_page=5, error_out=False)

        if not books.items:
            flash("No books found with the given title or ISBN.", "info")
        elif books.total == 0:
            flash("No results found.", "info")

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
            available_copies=total_copies,
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
        if not student.items:
            flash("No student found with the given matric number.", "info")
        elif student.total == 0:
            flash("No results found.", "info")
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

        try:
            filename = secure_filename(img_upload.filename)
            img_ext = filename.split(".")[-1].lower()
            random_number = secrets.token_hex(10)
            random_filename = f"{random_number}.{img_ext}"

            images.save(img_upload, name=random_filename)

            student = Student(
                name=name,
                matric_no=matric_no,
                department=department,
                email=email,
                img_upload=random_filename,
                student_status=student_status,
            )
            student.generate_password_hash(password)
            db.session.add(student)
            db.session.commit()

            flash("Student added successfully", "success")
            return redirect(url_for("librarian.students"))

        except Exception as e:
            flash(f"An error occurred while adding a new student: {str(e)}", "danger")
            return redirect(url_for("librarian.add_student"))

    return render_template("librarian/add_student.html", form=form)


@librarian.route("/librarian/view_student/<int:student_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("librarian/view_student.html", student=student)


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
        student.updated_at = datetime.now()
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
    form = SearchForm()
    issue = Issue.query.order_by(Issue.issued_date.desc()).paginate(
        per_page=5, error_out=False
    )
    return render_template("librarian/issued_book.html", issue=issue, form=form)


@librarian.route("/librarian/issued_book/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_issue():
    form = SearchForm()
    issue = None

    if form.validate_on_submit():
        query = form.query.data.strip()
        try:
            # Convert the user input into a valid date
            issued_date = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "warning")
            return render_template("librarian/issued_book.html", form=form, issue=issue)

        issue = Issue.query.filter(
            db.func.date(Issue.issued_date) == issued_date
        ).paginate(per_page=10, error_out=False)

        if not issue.items:
            flash("No issue found with the given issued date.", "info")
        elif issue.total == 0:
            flash("No results found.", "info")

    return render_template("librarian/issued_book.html", form=form, issue=issue)


@librarian.route("/librarian/issue_book", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def issue_book():
    form = IssueBookForm()
    if form.validate_on_submit():
        book_id = form.book_isbn.data
        student_id = form.matric_no.data
        librarian_id = current_user.id

        book_id = Book.query.filter(
            Book.isbn == book_id, Book.available_copies > 0
        ).first()
        student_id = Student.query.filter_by(matric_no=student_id).first()
        if not book_id:
            flash("Book is not available for issue", "danger")
            return redirect(url_for("librarian.issue_book"))
        book_id.available_copies -= 1
        book_id, student_id = book_id.id, student_id.id

        issued_book = Issue(
            student_id=student_id, book_id=book_id, librarian_id=librarian_id
        )
        issued_book.set_expiry_date(datetime.utcnow())
        db.session.add(issued_book)

        try:
            db.session.commit()
            flash("Book issued successfully", "success")
            return redirect(url_for("librarian.issued_book"))
        except Exception as e:
            flash(f"An error occurred while issuing a book: {str(e)}", "danger")
            return redirect(url_for("librarian.issued_book"))
    return render_template("librarian/issue_book.html", form=form)


@librarian.route("/librarian/return_book/<int:issue_id>", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def return_book(issue_id):
    id = issue_id
    issue_id = Issue.query.get_or_404(id)

    issue_id = issue_id.id
    issue = Issue.query.filter_by(id=issue_id).first()

    book_id = issue.book_id
    book = Book.query.filter_by(id=book_id).first()
    book_isbn = book.isbn
    book_title = book.title

    student_id = issue.student_id
    student = Student.query.filter_by(id=student_id).first()
    matric_no = student.matric_no
    print(issue.return_date)
    librarian_id = current_user.name
    if request.method == "POST":
        if issue.return_date:
            flash("Book already returned", "danger")
            return redirect(url_for("librarian.return_book", issue_id=id))

        fine_amount = calculate_fine(issue.expiry_date)
        if fine_amount > 0:
            fine = Fine(
                amount=fine_amount, student_id=student.id, matric_no=student.matric_no
            )
            db.session.add(fine)
            db.session.commit()

            fine_id = fine.id
            issue.add_fine_to_student(fine_id)

        book.available_copies += 1
        issue.returned_date(datetime.utcnow())
        try:
            db.session.commit()
            flash("Book returned successfully", "success")
        except Exception as e:
            flash(f"An error occurred while returning a book: {str(e)}", "danger")
    return render_template(
        "librarian/return_book.html",
        book_title=book_title,
        book_isbn=book_isbn,
        matric_no=matric_no,
        librarian_id=librarian_id,
        id=id,
    )


""" Fine section"""


@librarian.route("/librarian/fine", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def fine():
    form = SearchForm()
    fine = Fine.query.order_by(Fine.student_id).paginate(per_page=5, error_out=False)
    return render_template("librarian/fine.html", fine=fine, form=form)


"""Fine  search section"""


@librarian.route("/librarian/fine/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_fine():
    form = SearchForm()
    fine = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        fine = Fine.query.filter(Fine.matric_no.ilike(f"%{query}%")).paginate(
            per_page=10, error_out=False
        )
        if not fine.items:
            flash("No fine found with the given matric number.", "info")
        elif fine.total == 0:
            flash("No results found.", "info")
    return render_template("librarian/fine.html", form=form, fine=fine)


""" Reserve section"""


@librarian.route("/librarian/reserve", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def reserve():
    form = SearchForm()
    reserve = Reservation.query.order_by(Reservation.reservation_date.desc()).paginate(
        per_page=5, error_out=False
    )
    return render_template("librarian/reserve.html", reserve=reserve, form=form)


"""Reserve  search section"""


@librarian.route("/librarian/reserve/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
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
            return render_template("librarian/reserve.html", form=form, reserve=reserve)

        reserve = Reservation.query.filter(
            db.func.date(Reservation.reservation_date) == reservation_date
        ).paginate(per_page=10, error_out=False)

        if not reserve.items:
            flash("No Book reservation found with the given date or status.", "info")
        elif reserve.total == 0:
            flash("No results found.", "info")
    return render_template("librarian/reserve.html", form=form, reserve=reserve)


""" image upload section"""


@librarian.route("/upload/<path:filename>")
@session_expired_handler("librarian")
def upload(filename):
    return send_from_directory(
        current_app.config["UPLOADED_IMAGES_DEST"], filename, as_attachment=True
    )


""" generate library card for student section"""


@librarian.route("/librarian/student_library_card/<int:student_id>")
@session_expired_handler("librarian")
def student_library_card(student_id):
    student = Student.query.get(student_id)
    if student is None:
        flash("Student not found", "warning")
        return redirect(url_for("librarian.students"))
    image_buffer = generate_library_card(student.id)
    if image_buffer is None:
        flash("unable to generate library card buffer not found", "warning")
        return redirect(url_for("librarian.students"))

    try:
        library_card = LibraryCard(student_id=student.id)
        library_card.set_expiry_date()
        db.session.add(library_card)
        student.library_card_generated = True
        db.session.commit()
    except Exception as e:
        flash(f"An error occurred while generating library card: {str(e)}", "danger")
        return redirect(url_for("librarian.students"))

    return send_file(
        image_buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"{student.matric_no}_library_card.png",
    )


""" Transaction section"""


@librarian.route("/librarian/transaction", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def transaction():
    form = SearchForm()

    payment = Payment.query.order_by(Payment.id).paginate(per_page=5, error_out=False)

    return render_template("librarian/transaction.html", payment=payment, form=form)


""" search section"""


@librarian.route("/librarian/transaction/search", methods=["GET", "POST"])
@session_expired_handler("librarian")
@role_required("librarian")
def search_transaction():
    form = SearchForm()
    payment = None
    if form.validate_on_submit():
        query = form.query.data.lower().strip()
        try:
            # Convert the user input into a valid date
            payment_date = datetime.strptime(query, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "warning")
            return render_template(
                "librarian/transaction.html", form=form, payment=payment
            )

        payment = Payment.query.filter(
            (db.func.date(Payment.payment_date) == payment_date)
        ).paginate(per_page=10, error_out=False)
        if not payment.items:
            flash("No payment found with the given transaction details.", "info")
        elif payment.total == 0:
            flash("No results found.", "info")

    return render_template("librarian/transaction.html", form=form, payment=payment)
