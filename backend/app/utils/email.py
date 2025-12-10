
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # For local dev

MAILERSEND_API_TOKEN = getenv("MAILERSEND_API_TOKEN")
SMTP_HOST = getenv("SMTP_HOST", "smtp.mailersend.net")
SMTP_PORT = int(getenv("SMTP_PORT", "587"))
SMTP_USERNAME = getenv("SMTP_USER")  # e.g., MS_xxx@findmydreamjobs.com
DISPLAY_NAME = "Findmydreamjobs Team"
SMTP_PASSWORD = getenv("SMTP_PASS")
FROM_EMAIL = getenv("FROM_EMAIL", "noreply@example.com")
ENVIRONMENT = getenv("Env", "dev")  # Use "production" in Render
FRONTEND_URL = getenv("FRONTEND_BASE_URL", "https://findmydreamjobs.com")  # Fallback for safety


# Main wrapper function
def send_password_reset_email(email: str, token: str):
    reset_url = f"{FRONTEND_URL}/login/reset-password?token={token}"
    subject = "Reset Your Password"
    body = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>You requested a password reset. Click the link below to reset your password:</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>If you didn't request this, you can safely ignore this email.</p>
        <p>– The FindMyDreamJobs Team</p>
      </body>
    </html>
    """

    if ENVIRONMENT == "production":
        send_with_mailersend(email, subject, body)
    else:
        send_with_smtp(email, subject, body)

# Option 1: SMTP (Local Dev)
def send_with_smtp(to_email: str, subject: str, html_body: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{DISPLAY_NAME} <{SMTP_USERNAME}>"
        msg["To"] = to_email

        part = MIMEText(html_body, "html")
        msg.attach(part)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        print(f"✅ [SMTP] Email sent to {to_email}")
    except Exception as e:
        print(f"❌ [SMTP] Failed to send email: {e}")

# Option 2: MailerSend API (Production)
def send_with_mailersend(to_email: str, subject: str, html_body: str):
    try:
        headers = {
            "Authorization": f"Bearer {MAILERSEND_API_TOKEN}",
            "Content-Type": "application/json",
        }

        data = {
            "from": {
                "email": SMTP_USERNAME,
                "name": DISPLAY_NAME
            },
            "to": [{"email": to_email}],
            "subject": subject,
            "html": html_body,
        }

        response = requests.post("https://api.mailersend.com/v1/email", headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ [MailerSend] Email sent to {to_email}")
    except requests.exceptions.RequestException as e:
        print(f"❌ [MailerSend] Failed to send email: {e}")
