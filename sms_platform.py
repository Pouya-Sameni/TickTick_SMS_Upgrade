import email
import smtplib
import ssl
from sms_mms_providers import PROVIDERS
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_sms_via_email(
    number: str,
    message: str,
    subject: str = "",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
    provider="Bell Canada"
):

    sender_credentials = (config('emailUser'), config('emailPass'))

    sender_email, email_password = sender_credentials

    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
    
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = message

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(msg['From'], msg['To'], msg.as_string())
