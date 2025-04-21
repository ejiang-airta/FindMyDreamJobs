# File: backend/app/utils/email.py
# This code is responsible for sending password reset emails to users.

import smtplib
from email.mime.text import MIMEText
from os import getenv


SMTP_USER = getenv("SMTP_USER")
SMTP_PASS = getenv("SMTP_PASS")
SMTP_HOST = getenv("SMTP_HOST", "smtp.mailersend.net")
SMTP_PORT = int(getenv("SMTP_PORT", "587"))

def send_password_reset_email(email: str, token: str):
    FRONTEND_URL = getenv("FRONTEND_URL", "http://localhost:3000")
    reset_url = f"{FRONTEND_URL}/login/reset-password?token={token}"


    message = MIMEText(f"Click the link below to reset your password:\n\n{reset_url}")
    message["Subject"] = "Reset your password"
    message["From"] = SMTP_USER
    message["To"] = email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, email, message.as_string())
