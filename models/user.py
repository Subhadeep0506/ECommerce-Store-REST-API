from typing import Dict, Union
from requests import Response, post
from flask import request, url_for

from database import db
from libs.mailgun import Mailgun


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

        subject = "CONFIRM REGISTRATION"
        text = f"Click the link to confirm ragistration: {link}"
        html = f'<html>Click the link to confirm ragistration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
