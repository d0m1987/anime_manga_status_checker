# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

def send_message(html_body:str):
    message = Mail(
        from_email=config("USER_EMAIL"),
        to_emails=config("USER_EMAIL"),
        subject='Update HTML Update Checker',
        html_content=html_body)
    try:
        sg = SendGridAPIClient(config("SENDGRID_API_KEY"))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.error(e.message)