import sqlite3

from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

  parser = reqparse.RequestParser()
  parser.add_argument("price",
    type=float,
    required=True,
    help="This field cannot be blank"
  )
  
  # searches the database for items using name
  @classmethod
  def find_item_by_name(cls, name):
    connection = sqlite3.connect('./test/data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM items WHERE name=?"
    result = cursor.execute(query, (name,))

    row = result.fetchone()
    connection.close()

    if row:
        return {
            "item": {
                "name": row[0],
                "price": row[1]
            }
        }

  # method to insert an item into
  @classmethod
  def insert(cls, item):
    connection = sqlite3.connect("./test/data.db")
    cursor = connection.cursor()

    query = "INSERT INTO items VALUES (?, ?)"
    cursor.execute(query, (item["name"], item["price"]))

    connection.commit()
    connection.close()

  # TO GET ITEM WITH NAME
  @jwt_required()
  def get(self, name):
    item = self.find_item_by_name(name)
    if item:
      return item
    
    return {"message": "item not found."}, 404

  # TO POST AN ITEM
  def post(self, name):
    # if there already exists an item with "name", show a messege, and donot add the item
    if self.find_item_by_name(name):
      return {"messege": f"item {name} already exists"} ,400

    data = Item.parser.parse_args()
    # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    item = {                      # flask will look into the content, and format the data.
      "name": name,
      "price": data["price"]
    }

    try:
      self.insert(item)
    except:
      return {"messege": "An error occured."}
    
    return item, 201  # 201 is for CREATED status

  # TO DELETE AN ITEM
  def delete(self, name):
    # check if there exists any item by name: "name"
    # if exists then delete it
    if self.find_item_by_name(name):
      connection = sqlite3.connect("./test/data.db")
      cursor = connection.cursor()

      query = "DELETE FROM items WHERE name=?"
      cursor.execute(query, (name,))

      connection.commit()
      connection.close()
      return {"messege": "Item deleted"}

    # if doesn't exist, skip deleting
    return {"messege": "Item don't exist"}, 400

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
    items = []
    connection = sqlite3.connect("./test/data.db")
    cursor = connection.cursor()

    query = "SELECT * FROM items"
    for row in cursor.execute(query):
      items.append({"name": row[0], "price": row[1]})

    connection.commit()
    connection.close()
    return {"items": items}