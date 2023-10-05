import io
import os
import random
from datetime import datetime, timedelta

from flask import current_app, make_response
from PIL import Image, ImageDraw, ImageFont

from lms.encryption import decode_jwt
from lms.models import Librarian, Student


# function to handle the login token
def handle_login(token):
    ok, data = decode_jwt(token)

    if ok:
        role = data.get("role")
        alternative_id = data.get("id")

        if role == "admin":
            admin = Librarian.query.filter(
                Librarian.alternative_id == alternative_id,
                Librarian.is_admin == True,
            ).first()
            if admin:
                return admin

        elif role == "librarian":
            librarian = Librarian.query.filter(
                Librarian.alternative_id == alternative_id,
                Librarian.is_librarian == True,
            ).first()
            if librarian:
                return librarian

        elif role == "student":
            student = Student.query.filter_by(alternative_id=alternative_id).first()
            if student:
                return student

    return None


# function to handle the token authentication
def token_authentication(request) -> str:
    # check for the cookie token
    cookie_token = request.cookies.get("token")
    if cookie_token:
        return handle_login(cookie_token)


# function to set cookie
def set_cookie(response: make_response, token, duration=3600) -> make_response:
    cookie = dict()

    cookie["key"] = "token"
    cookie["value"] = token
    cookie["max_age"] = duration

    response.set_cookie(**cookie)
    return response


# function to calculate fine
def calculate_fine(issue_expiry_date):
    current_date = datetime.utcnow()
    if current_date > issue_expiry_date:
        days_overdue = (current_date - issue_expiry_date).days
        print(days_overdue)

        fine_per_day = 100  # Adjust this to your fine rate per day
        fine_amount = fine_per_day * days_overdue
        amount = fine_amount
        return amount
    else:
        amount = 0
        return amount


# function to generate library card
def generate_library_card(student_id: int) -> int:
    student = Student.query.get(student_id)

    name = student.name
    matric_no = student.matric_no
    department = student.department
    img_upload = student.img_upload
    expire_date = datetime.utcnow() + timedelta(days=365)
    expire_date = expire_date.strftime("%Y-%m-%d")
    

    card_img_location = os.path.join(
        current_app.root_path, "assets/images/library_card_template_front.png"
    )
    card_template = Image.open(card_img_location)

    student_img_location = os.path.join(current_app.root_path, f"upload/{img_upload}")
    student_img = Image.open(student_img_location).resize(size(20.54, 26.87))

    card_template.paste(student_img, size(5.37, 9.02))

    draw = ImageDraw.Draw(card_template)
    font = os.path.join(
        current_app.root_path, "assets/fonts/feather/fonts/BalsamiqSans-Regular.ttf"
    )
    font = ImageFont.truetype(font, size=20)

    draw.text(size(44.07, 28.4), name, fill=(0, 0, 0), font=font)
    draw.text(size(44.07, 35.0), matric_no, fill=(0, 0, 0), font=font)
    draw.text(size(44.07, 41.5), department, fill=(0, 0, 0), font=font)
    draw.text(size(44.07, 48.0), expire_date, fill=(0, 0, 0), font=font)

    card_template.save(
        os.path.join(current_app.root_path, "assets/images/library_card.png")
    )

    image_buffer = io.BytesIO()
    card_template.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    return image_buffer

# Function to calculate target size in pixels
def size(target_width_mm:float, target_height_mm:float) -> tuple[int, int]:
    dpi = 300
    target_width = int(target_width_mm * dpi / 25.4)
    target_height = int(target_height_mm * dpi / 25.4)
    
    return target_width, target_height
 
    