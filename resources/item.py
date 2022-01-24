import sqlite3

from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

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
    item = ItemModel.find_item_by_name(name)
    if item:
      return item.json()
    
    return {"message": "item not found."}, 404

  # TO POST AN ITEM
  def post(self, name):
    # if there already exists an item with "name", show a messege, and donot add the item
    if ItemModel.find_item_by_name(name):
      return {"messege": f"item {name} already exists"} ,400

    data = Item.parser.parse_args()
    # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    item = ItemModel(name, data["price"])

    try:
      item.insert()
    except:
      return {"messege": "An error occured."}, 500
    
    return item.json(), 201  # 201 is for CREATED status

  # TO DELETE AN ITEM
  @jwt_required()
  def delete(self, name):
    # check if there exists any item by name: "name"
    # if exists then delete it
    if ItemModel.find_item_by_name(name):
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
    item = ItemModel.find_item_by_name(name)

    updated_item = ItemModel(name, data["price"])
    # if item is not available, add it
    if item is None:
      try:
        updated_item.insert()
      except:
        return {"message": "An error occured while inserting."}, 500
    # if item exists, update it
    else:
      try:
        updated_item.update()
      except:
        return {"message": "An error occured while updating."}, 500

    return updated_item.json()


class ItemList(Resource):

  # TO GET ALL ITEMS
  def get(self):
    items = []
    connection = sqlite3.connect("./test/data.db")
    cursor = connection.cursor()

    query = "SELECT * FROM items"
    for row in cursor.execute(query):
      items.append({"name": row[0], "price": row[1]})

    connection.close()
    return {"items": items}