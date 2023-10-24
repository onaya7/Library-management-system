import getpass

from flask.cli import FlaskGroup

from lms.models import Librarian, db
from wsgi import app

cli = FlaskGroup(app)

@cli.command("create_admin")
def create_admin():
    """Creates an admin user."""
    print("Creating an Admin user...")
    print("Press Ctrl-C to abort.")
    input("Press Enter to continue...")

    name = input("Enter your full name: ")
    password = getpass.getpass("Enter your password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return 1
    email = input("Enter your email: ")
    phone = input("Enter your phone (eg, 08167579402): ")
    try:
        librarian = Librarian(name=name,email=email, phone=phone)
        librarian.generate_password_hash(password)
        db.session.add(librarian)
        db.session.commit()
    except Exception as e:
        print(f"Error creating admin user: {e}")
    print(f"Admin user {name} created successfully.")


if __name__ == "__main__":
    cli()
