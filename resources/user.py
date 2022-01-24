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
    
    # else...continue
    # 1. Connect to database
    connection = sqlite3.connect('./test/data.db')
    # 2. Create database cursor
    cursor = connection.cursor()
    # 3. SQL query to inser new useer information
    query = "INSERT INTO users VALUES (NULL, ?, ?)"

    cursor.execute(query, (data["username"], data["password"]))
    # 4. Commit the changes and close the connection to database
    connection.commit()
    connection.close()

    return {"messege": "User added successfully."}, 201