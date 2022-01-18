from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
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