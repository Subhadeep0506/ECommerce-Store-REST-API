import sqlite3
from flask_restful import Resource, reqparse

class User:

  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password
    
  @classmethod
  def find_by_username(cls, username):
    connection = sqlite3.connect('./test/data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username=?"
    result = cursor.execute(query, (username,))   # parameters must be in the form of tuple.

    row = result.fetchone()
    if row:
      # user = cls(row[0], row[1], row[2])
      user = cls(*row)  # is similar to passing all values of row
    else:
      user = None

    connection.close()
    return user

  @classmethod
  def find_by_id(cls, _id):
    connection = sqlite3.connect('./test/data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE id=?"
    result = cursor.execute(query, (_id,))   # parameters must be in the form of tuple.

    row = result.fetchone()
    if row:
      # user = cls(row[0], row[1], row[2])
      user = cls(*row)  # is similar to passing all values of row
    else:
      user = None

    connection.close()
    return user

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
    if User.find_by_username(data["username"]):
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