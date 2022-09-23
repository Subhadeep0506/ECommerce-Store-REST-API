from flask import request
from flask_restful import Resource

from models.item import ItemModel

ORDER_ITEM_BY_ID_NOT_FIND = "Item with id: '{}' was not found."


class Order(Resource):
    @classmethod
    def post(cls):
        # Expects a token and a list of item ids from request body.
        # Construct an order and  talk to Stripe API to make the purchase
        data = request.get_json()  # recieves token + list of item ids
        items = []

        for _id in data["item_ids"]:
            item = ItemModel.find_item_by_id(_id)
            if not item:
                return {"message": ORDER_ITEM_BY_ID_NOT_FIND.format(_id)}

            items.append(item)

        order = OrderModel(items=items, status="pending")
        order.save_to_database()
