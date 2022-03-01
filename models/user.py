from typing import Dict, Union
from requests import Response, post
from flask import request, url_for

from database import db

UserJSON = Dict[str, Union[int, str]]
# MAILGUN_DOMAIN = "YOUR_DOMAIN"
MAILGUN_DOMAIN = "sandbox2547fbe807ac4a6faa83edbd51fe6e93.mailgun.org"

# MAILGUN_API_KEY = "API_KEY_HERE"
MAILGUN_API_KEY = "fe5c954e9d180a06938ac17e71ab0240-e2e3d8ec-005737fa"

FROM_TITLE = "Stores RestAPI"

# FROM_EMAIL = "Your Mailgun Email"
FROM_EMAIL = "subhadeepdoublecap@gmail.com"


class UserModel(db.Model):

    __tablename__ = "users"  # will be used to tell sqlalchemy the table name for users

    # table columns for users table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    # This method will interact with Mailgun API and return the response sent
    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000 - is the 'url_root'
        # url_for("userconfirm") - this must mathch the name of user confirmation endpoint
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=(
                "api",
                MAILGUN_API_KEY,
            ),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": [self.email],
                "subject": "CONFIRM REGISTRATION",
                "text": f"Click the link to confirm ragistration: {link}",
            },
        )

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
