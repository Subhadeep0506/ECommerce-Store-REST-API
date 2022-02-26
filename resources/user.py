from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

# extracted parser variable for global use, and made it private
# _user_parser = reqparse.RequestParser()
# _user_parser.add_argument(
#   "username",
#   type=str,
#   required=True,
#   help="This field cannot be empty"
# )
# _user_parser.add_argument(
#   "password",
#   type=str,
#   required=True,
#   help="This field cannot be empty"
# )

user_schema = UserSchema()


# New user registration class
class UserRegister(Resource):

    # calls to post a new user (new user registration)
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        # First check if that user is present or not
        if UserModel.find_by_username(user.username):
            # if exists, then don't add
            return {"message": "An user with that username already exists."}, 400

        # user = UserModel(data["username"], data["password"])
        # user = UserModel(**user_data)  # since parser only takes in username and password, only those two will be added.
        # flask_marshmallow already creates a user model, so we need not do it manually
        user.save_to_database()

        return {"messege": "User added successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404

        user.delete_from_database()
        return {"message": "User deleted."}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        user_data = user_schema.load(request.get_json())

        # find user in database
        user = UserModel.find_by_username(user_data.username)

        # check password
        # this here is what authenticate() function used to do
        if user and safe_str_cmp(user.password, user_data.password):

            # create access and refresh tokens
            access_token = create_access_token(identity=user.id, fresh=True)  # here, identity=user.id is what identity() used to do previously
            refresh_token = create_refresh_token(identity=user.id)
            print("user logged in")

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials."}, 401  # Unauthorized


class UserLogout(Resource):
    # Loggig out requirees jwt as if user is not logged in they cannot log out
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]  # jti is JWT ID, unique identifier for a JWT
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)  # fresh=Flase means that user have logged in days ago.

        return {"access_token": new_token}, 200
