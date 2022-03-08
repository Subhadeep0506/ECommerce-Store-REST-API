from time import time
import traceback
from flask_restful import Resource
from flask import make_response, render_template

from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema
from libs.mailgun import MailgunException

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    # Returns confirmation HTML page
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": "Confirmation referrence not found"}, 404

        if confirmation.has_expired:
            return {"message": "Confirmation link has expired."}, 400

        if confirmation.confirmed:
            return {"message": "Registration has already been confirmed."}, 400

        confirmation.confirmed = True
        confirmation.save_to_database()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers,
        )


class ConfirmationByUser(Resource):
    # Return confirmations for given user. Only for test purpose
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404

        return {
            "current_time": int(time()),
            "confirmation": [confirmation_schema.dump(each) for each in user.confirmation.order_by(ConfirmationModel.expire_at)],
        }, 200

    # Resend confirmation email
    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "Registration has already been confirmed"}, 400

                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_database()
            user.send_confirmation_email()

            return {"message": "Confirmation mail re-send successful"}, 201

        except MailgunException as err:
            return {"message": str(err)}, 500
        except:
            traceback.print_exc()
            return {"message": "Failed to resend confirmation mail."}, 500
