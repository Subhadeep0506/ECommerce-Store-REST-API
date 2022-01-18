from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = "komraishumtirkomchuri"

api = Api(app)

# JWT() creates a new endpoint: /auth
# we send an username and password to /auth
# JWT() gets the username and password, and sends it to authenticate function
# the authenticate function maps the username and checks the password
# if all goes well, the authenticate function returns user
# which is the identity or jwt(or token)
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
  @jwt_required()
  def get(self, name):
    item = next(filter(lambda x: x["name"] == name, items), None)
    return {"item": item}, 200 if item else 404

  def post(self, name):
    # if there already exists an item with "name", show a messege, and donot add the item
    if next(filter(lambda x: x["name"] == name, items), None):
      return {"messege": f"item {name} already exists"} ,400

    data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    item = {                    # flask will look into the content, and format the data.
      "name": name,
      "price": data["price"]
    }
    items.append(item)
    return item, 201  # 201 is for CREATED status

class ItemList(Resource):
  def get(self):
    return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)