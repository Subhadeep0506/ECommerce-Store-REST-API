from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

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

  parser = reqparse.RequestParser()
  parser.add_argument("price",
    type=float,
    required=True,
    help="This field cannot be blank"
  )
  
  # TO GET ITEM WITH NAME
  @jwt_required()
  def get(self, name):
    item = next(filter(lambda x: x["name"] == name, items), None)
    return {"item": item}, 200 if item else 404

  # TO POST AN ITEM
  def post(self, name):
    # if there already exists an item with "name", show a messege, and donot add the item
    if next(filter(lambda x: x["name"] == name, items), None):
      return {"messege": f"item {name} already exists"} ,400

    data = Item.parser.parse_args()
    # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    item = {                      # flask will look into the content, and format the data.
      "name": name,
      "price": data["price"]
    }
    items.append(item)
    return item, 201  # 201 is for CREATED status

  # TO DELETE AN ITEM
  def delete(self, name):
    # use the items variable avalable globally
    global items
    # check if the item exists
    item = next(filter(lambda x: x["name"] == name ,items), None)
    # if doesn't exist, skip deleting
    if item is None:
      return {"messege": "Item don't exist"}, 400
    
    # store all the elements of items variable into local item
    # except the one that was selected to be deleted
    items = list(filter(lambda x: x["name"] != name, items))
    return {"messege": "Item deleted"}

  # TO ADD OR UPDATE AN ITEM
  def put(self, name):
    data = Item.parser.parse_args()
    # data = request.get_json()
    item = next(filter(lambda x: x["name"] == name ,items), None)
    # if item is not available, add it
    if item is None:
      item = {
        "name": name,
        "price": data["price"]
      }
      items.append(item)
    # if item exists, update it
    else:
      item.update(data)
    return item


class ItemList(Resource):

  # TO GET ALL ITEMS
  def get(self):
    return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)