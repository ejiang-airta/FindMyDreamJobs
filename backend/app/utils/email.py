# ✅ File: backend/app/utils/email.py
# Sends password reset emails using MailerSend SMTP with a friendly display name.

import smtplib
from email.mime.text import MIMEText
from os import getenv

SMTP_USER = getenv("SMTP_USER")  # e.g., MS_xxx@findmydreamjobs.com
SMTP_PASS = getenv("SMTP_PASS")
SMTP_HOST = getenv("SMTP_HOST", "smtp.mailersend.net")
SMTP_PORT = int(getenv("SMTP_PORT", "587"))
FRONTEND_URL = getenv("FRONTEND_BASE_URL", "https://findmydreamjobs.com")  # Fallback for safety

# Custom sender display name (used even if on Hobby plan)
DISPLAY_NAME = "Findmydreamjobs Team"

def send_password_reset_email(email: str, token: str):
    FRONTEND_URL = getenv("FRONTEND_BASE_URL")      # This should be set to the base URL of your frontend application
    reset_url = f"{FRONTEND_URL}/login/reset-password?token={token}"

    # Construct message
    body = f"""Hello,

You requested to reset your password.

Click the link below to reset it:
{reset_url}

If you did not request this, please ignore this message.

Best,
{DISPLAY_NAME}
"""
    message = MIMEText(body)
    message["Subject"] = "🔐 Reset Your Password"
    message["From"] = f"{DISPLAY_NAME} <{SMTP_USER}>"  # 👈 Friendly name + sender email
    message["To"] = email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, email, message.as_string())