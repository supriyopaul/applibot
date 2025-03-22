import smtplib
from email.message import EmailMessage

def send_reset_email(to_email: str, reset_url: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str, from_email: str = None):
    msg = EmailMessage()
    msg.set_content(f"Click the following link to reset your password: {reset_url}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = from_email if from_email else smtp_user
    msg['To'] = to_email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
