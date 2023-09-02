from lms.extensions import db
from datetime import datetime, timedelta

class Book(db.Model):
    __tablename__ = "book"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    book_category_id = db.Column(db.Integer, db.ForeignKey('book_category.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    isbn =  db.Column(db.Integer, nullable=False)
    img_upload = db.Column(db.String(100), nullable=False)
    total_copies = db.Column(db.Integer, default=0)
    available_copies = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"Book(id:'{self.id}', author_id:'{self.author_id}', title:'{self.title}')"
    

class BookCategory(db.Model):
    __tablename__ = "book_category"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)
    
    def __repr__(self):
        return f"BookCategory(id:'{self.id}', name:'{self.name}')"

class Author(db.Model):
    __tablename__ = "author"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)
    
    def __repr__(self):
        return f"Author(id:'{self.id}', name:'{self.name}')"
    
    
class Student(db.Model):
    __tablename__ = "student"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    matric_no = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    img_upload = db.Column(db.String(100), nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    student_status= db.Column(db.Boolean, default=True)
    library_card = db.relationship('LibraryCard', backref='student', uselist=False)
    fine = db.relationship('Fine', backref='student', uselist=False)

    def __repr__(self):
        return f"Student(id:'{self.id}', name:'{self.name}')"


class Librarian(db.Model):
    __tablename__ = "librarian"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    is_librarian = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    
    
    def __repr__(self):
        return f"Librarian(id:'{self.id}', name:'{self.name}')"
    
class LibraryCard(db.Model):
    __tablename__ = "librarycard"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.expiry_date = self.issued_date + timedelta(days=365)  # Adding one year

    def has_expired(self):
        return datetime.utcnow() > self.expiry_date
    
    def __repr__(self):
        return f"LibraryCard(id:'{self.id}', student_id:'{self.student_id}')"
    
    
class Reservation(db.Model):
    __tablename__ = "reservation"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    reservation_status= db.Column(db.Boolean, default=True)
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"Reservation(id:'{self.id}', book_id:'{self.book_id}', student_id:'{self.student_id}')"
    
class Issue(db.Model):
    __tablename__ = "issue"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    librarian_id = db.Column(db.Integer, db.ForeignKey('librarian.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='issue', lazy=True)
    
    def __repr__(self):
        return f"Issue(id:'{self.id}', book_id:'{self.book_id}', student_id:'{self.student_id}', librarian_id:'{self.librarian_id}')"



class Transaction(db.Model):
    __tablename__ = "transaction"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    fine_id = db.Column(db.Integer, db.ForeignKey('fine.id'), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.expiry_date = self.issued_date + timedelta(days=14)  # Adding 14 days

    def has_expired(self):
        return datetime.utcnow() > self.expiry_date
    
    def returned_date(self, date):
        self.return_date = date
        
    def __repr__(self):
        return f"Transaction(id:'{self.id}', book_id:'{self.book_id}', student_id:'{self.student_id}', fine_id:'{self.fine_id}')"
    

class Fine(db.Model):
    __tablename__ = "fine"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=2000)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='issue', lazy=True)

    def calculate_fine(self):
        expiration_date = self.transactions[0].expiry_date
        current_date = datetime.utcnow()
        
        days_overdue = (current_date - expiration_date).days
        
        if days_overdue > 0:
            fine_per_day = 100
            fine_amount = fine_per_day * days_overdue 
            return fine_amount
        else:
            return 0
    def __repr__(self):
        return f"Fine(id:'{self.id}', amount:'{self.amount}', student_id:'{self.student_id}')"


class Payment(db.Model):
    __tablename__ = "payment"
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='issue', lazy=True)
    amount = db.Column(db.Float, nullable=False )
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Payment(id:'{self.id}', amount:'{self.amount}', student_id:'{self.student_id}')"



    
