from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # turns of flask_sqlalchemy modification tracker
app.config["PROPAGATE_EXCEPTIONS"] = True   # if flask_jwt raises an error, the flask app will check the error if this is set to true
app.secret_key = "komraishumtirkomchuri"
# app.config["JWT_SECRET_KEY"] = "YOUR KEY HERE"

api = Api(app)

@app.before_first_request
def create_tables():
  db.create_all()
  # above function creates all the tables before the 1st request is made
  # unless they exist alraedy

# JWT() creates a new endpoint: /auth
# we send an username and password to /auth
# JWT() gets the username and password, and sends it to authenticate function
# the authenticate function maps the username and checks the password
# if all goes well, the authenticate function returns user
# which is the identity or jwt(or token)
# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)   # JwtManager links up to the application, doesn't create /auth point

@jwt.additional_claims_loader   # modifies the below function, and links it with JWTManager, which in turn is linked with our app
def add_claims_to_jwt(identity):
  if identity == 1:   # insted of hardcoding this, we should read it from a config file or database
    return {"is_admin": True}
  
  return {"is_admin": False}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == "__main__":
  db.init_app(app)
  app.run(port=5000, debug=True)