import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
# New user registraction class
class UserRegister(Resource):
  # Creating a request parser
  parser = reqparse.RequestParser()
  # Adding username argument to parser
  parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be empty"
  )
  # Adding password argument to parser
  parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be empty"
  )

  # calls to post a new user (new user registration)
  def post(self):
    data = UserRegister.parser.parse_args()
    # First check if that user is present or not
    if UserModel.find_by_username(data["username"]):
      # if exists, then don't add
      return {"message": "An user with that username already exists."}, 400
    
    user = UserModel(**data)  # since parser only takes in username and password, only those two will be added.
    user.save_to_database()

    return {"messege": "User added successfully."}, 201