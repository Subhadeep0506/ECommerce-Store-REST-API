from typing import Dict
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank"
ITEM_NOT_FOUND = "item not found."
NAME_ALREADY_EXISTS = "item '{}' already exists"
ERROR_INSERTING = "An error occured while inserting the item."
ITEM_DELETED = "Item deleted"


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help=BLANK_ERROR.format("price"),
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help=BLANK_ERROR.format("store_id"),
    )

    # TO GET ITEM WITH NAME
    @classmethod
    @jwt_required()
    def get(cls, name: str) -> Dict:
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json(), 200

        return {"message": ITEM_NOT_FOUND}, 404

    # TO POST AN ITEM
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        # if there already exists an item with "name", show a messege, and donot add the item
        if ItemModel.find_item_by_name(name):
            return {"messege": NAME_ALREADY_EXISTS.format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
        item = ItemModel(name, **data)

        try:
            item.save_to_database()
        except:
            return {"messege": ERROR_INSERTING}, 500

        return item.json(), 201  # 201 is for CREATED status

    # TO DELETE AN ITEM
    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        claims = get_jwt()

        if not claims["is_admin"]:
            return {"message": "Admin privilages required"}, 401

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_database()
            return {"messege": ITEM_DELETED}

        # if doesn't exist, skip deleting
        return {"messege": ITEM_NOT_FOUND}, 400

    # TO ADD OR UPDATE AN ITEM
    @classmethod
    def put(cls, name: str):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel.find_item_by_name(name)

        # if item is not available, add it
        if item is None:
            item = ItemModel(name, **data)
        # if item exists, update it
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        # whether item is changed or inserted, it has to be saved to db
        item.save_to_database()
        return item.json()


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]

        # if user id is given, then display full details
        if user_id:
            return {"items": items}, 200

        # else display only item name
        return {
            "items": [item["name"] for item in items],
            "message": "Login to view more data.",
        }, 200
