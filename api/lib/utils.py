from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta ,timezone
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Secret key for JWT signing 
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token creation
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Email sending utility 
def send_email(to_email: str, subject: str, message: str):
    SMTP_SERVER = os.getenv("smtp_server")
    SMTP_PORT = 587
    SMTP_USER = os.getenv("smtp_user")
    SMTP_PASSWORD = os.getenv("smtp_password")

    try:
        msg = MIMEMultipart()
        msg['From'] = "sai1290.500apps@gmail.com"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

# Send welcome email on sign up
def send_welcome_email(to_email: str):
    subject = "Welcome to the platform"
    message = "Thank you for signing up. We're happy to have you!"
    send_email(to_email, subject, message)

# Send password reset email
def send_password_reset_email(to_email: str, new_password: str):
    subject = "Your Password Has Been Reset"
    message = f"Your new password is: {new_password}"
    send_email(to_email, subject, message)

# Send invitation email
def send_invite_email(to_email: str):
    subject = "You're Invited to Join Our Organization"
    message = "Click here to accept the invitation."
    send_email(to_email, subject, message)

# Utility to generate a random password 
import random
import string

def generate_random_password(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
