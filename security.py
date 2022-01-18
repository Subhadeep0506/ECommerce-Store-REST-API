from werkzeug.security import safe_str_cmp
from user import User

users = [
  User(1, "bob", "1234")
]

username_mapping = {u.username: u for u in users}   # mapping the users using set comprehension

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
  user = username_mapping.get(username, None)
  # if user and user.password == password:
  if user and safe_str_cmp(user.password, password):
    return user

def identity(payload):  # payload is the contents of jwt
  userid = payload["identity"]
  return userid_mapping.get(userid, None)
