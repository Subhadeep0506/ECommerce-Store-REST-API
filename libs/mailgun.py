import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")  # can be None
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")  # can be None
    FROM_TITLE = "Stores RestAPI"
    # FROM_EMAIL = "Your Mailgun Email"
    FROM_EMAIL = "postmaster@sandboxb3ef8f2c0e20406cb3f834bc39735ab4.mailgun.org"

    # This method will interact with Mailgun API and return the response sent
    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException("Falied to load Mailgun API key.")

        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException("Failde to load Mailgun domain.")

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=(
                "api",
                cls.MAILGUN_API_KEY,
            ),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailgunException("Error in sending confirmation email, user registration failed.")

        return response
