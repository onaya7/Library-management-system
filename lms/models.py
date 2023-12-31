import uuid
from datetime import datetime, timedelta

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import LargeBinary

from lms.encryption import decode_jwt, generate_jwt
from lms.extensions import db


def generate_alternative_id():
    return str(uuid.uuid4())
class Book(UserMixin, db.Model):
    __tablename__ = "book"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    book_category_id = db.Column(
        db.Integer, db.ForeignKey("book_category.id"), nullable=False
    )
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    img_upload = db.Column(db.String(100), nullable=False)
    total_copies = db.Column(db.Integer, nullable=True)
    available_copies = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=True)
    category = db.relationship("BookCategory", back_populates="books")
    author = db.relationship("Author", back_populates="books")
    issue = db.relationship("Issue", back_populates="books")
    reserve = db.relationship("Reservation", back_populates="books")

    def edit_book_details(
        self,
        book_category_id,
        author_id,
        title,
        description,
        version,
        publisher,
        isbn,
        img_upload,
        total_copies,
    ):
        self.book_category_id = book_category_id
        self.author_id = author_id
        self.title = title
        self.description = description
        self.version = version
        self.publisher = publisher
        self.isbn = isbn
        self.img_upload = img_upload
        self.total_copies = total_copies
        self.available_copies += total_copies
        self.updated_date = datetime.utcnow()

    def __repr__(self):
        return (
            f"Book(id:'{self.id}', author_id:'{self.author_id}', title:'{self.title}')"
        )


class BookCategory(UserMixin, db.Model):
    __tablename__ = "book_category"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship("Book", back_populates="category")

    def __repr__(self):
        return f"BookCategory(id:'{self.id}', name:'{self.name}')"


class Author(UserMixin, db.Model):
    __tablename__ = "author"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship("Book", back_populates="author", lazy=True)

    def __repr__(self):
        return f"Author(id:'{self.id}', name:'{self.name}')"


class Student(UserMixin, db.Model):
    __tablename__ = "student"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    alternative_id = db.Column(db.String(36), default=generate_alternative_id, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(LargeBinary, nullable=True)
    matric_no = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    img_upload = db.Column(db.String(100), nullable=False, default="profile.png")
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    student_status = db.Column(db.Boolean, default=True)
    library_card_generated = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=True)
    library_card = db.relationship("LibraryCard", back_populates="student")
    fine = db.relationship("Fine", back_populates="student")
    issue = db.relationship("Issue", back_populates="student")
    reserve = db.relationship("Reservation", back_populates="student")
    payment = db.relationship("Payment", back_populates="student")
    library_card = db.relationship("LibraryCard", back_populates="student")

        
    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

    def generate_jwt(self, exp) -> str:
        payload = dict()
        payload["id"] = self.alternative_id
        payload["role"] = "student"
        payload["exp"] = exp
        payload["iat"] = datetime.utcnow()

        return generate_jwt(payload)

    def get_id(self):
        try:
            return str(self.id)
        except Exception as e:
            return e

    def __repr__(self):
        return f"Student(id:'{self.id}', name:'{self.name}')"


class Librarian(UserMixin, db.Model):
    __tablename__ = "librarian"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    alternative_id = db.Column(db.String(36), default=str(uuid.uuid4()), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(LargeBinary, nullable=True)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    is_librarian = db.Column(db.Boolean, default=True)
    issue = db.relationship("Issue", back_populates="librarian")

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

    def generate_jwt(self, exp) -> str:
        payload = dict()
        payload["id"] = self.alternative_id
        payload["role"] = "librarian"
        payload["exp"] = exp
        payload["iat"] = datetime.utcnow()

        return generate_jwt(payload)

    @staticmethod
    def decode_jwt(
        token: str,
    ) -> tuple:
        return decode_jwt(token)

    def get_id(self):
        try:
            return str(self.id)
        except Exception as e:
            return e

    def __repr__(self):
        return f"Librarian(id:'{self.id}', name:'{self.name}')"


class LibraryCard(UserMixin, db.Model):
    __tablename__ = "librarycard"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)
    student = db.relationship("Student", back_populates="library_card", lazy=True)

    def set_expiry_date(self):
        self.expiry_date = datetime.utcnow() + timedelta(days=365)  # Adding one year

    def has_expired(self):
        return datetime.utcnow > self.expiry_date

    def __repr__(self):
        return f"LibraryCard(id:'{self.id}', student_id:'{self.student_id}')"


class Issue(UserMixin, db.Model):
    __tablename__ = "issue"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    fine_id = db.Column(db.Integer, db.ForeignKey("fine.id"), nullable=True)
    librarian_id = db.Column(db.Integer, db.ForeignKey("librarian.id"), nullable=True)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    student = db.relationship("Student", back_populates="issue")
    books = db.relationship("Book", back_populates="issue")
    fine = db.relationship("Fine", back_populates="issue")
    librarian = db.relationship("Librarian", back_populates="issue")
    payment = db.relationship("Payment", back_populates="issue")

    def add_fine_to_student(self, fine):
        self.fine_id = fine

    def set_expiry_date(self, date):
        self.expiry_date = date + timedelta(days=1)  # Expires in 1day

    def has_expired(self):
        return datetime.utcnow() > self.expiry_date

    def returned_date(self, date):
        self.return_date = date

    def __repr__(self):
        return f"Issue(id:'{self.id}', book_id:'{self.book_id}', student_id:'{self.student_id}', librarian_id:'{self.librarian_id}')"


class Fine(UserMixin, db.Model):
    __tablename__ = "fine"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=0)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    matric_no = db.Column(db.String(20))
    status = db.Column(db.Boolean, default=False)
    student = db.relationship("Student", back_populates="fine")
    issue = db.relationship("Issue", back_populates="fine")

    def __repr__(self):
        return f"Fine(id:'{self.id}', amount:'{self.amount}', student_id:'{self.student_id}')"


class Reservation(UserMixin, db.Model):
    __tablename__ = "reservation"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    reservation_status = db.Column(db.Boolean, default=True)
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship("Book", back_populates="reserve")
    student = db.relationship("Student", back_populates="reserve")

    def __repr__(self):
        return f"Reservation(id:'{self.id}', book_id:'{self.book_id}', student_id:'{self.student_id}')"


class Payment(UserMixin, db.Model):
    __tablename__ = "payment"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    transaction_id = db.Column(db.Integer, nullable=False)
    transaction_ref = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(60), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship("Student", back_populates="payment", lazy=True)
    issue = db.relationship("Issue", back_populates="payment", lazy=True)

    def __repr__(self):
        return f"Payment(id:'{self.id}', amount:'{self.amount}', issue_id:'{self.issue_id}')"
