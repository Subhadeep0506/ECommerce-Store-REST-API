from flask import Flask, jsonify, request, render_template
# creating an app from Flask class
app = Flask(__name__)

stores = [
  {
    "name": "My store",
    "items": [
      {
        "name": "My item",
        "price": 12.99
      }
    ]
  }
]

@app.route('/')
def home():
  return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_store = {
    'name': request_data['name'],
    'items': [],
  }
  stores.append(new_store)
  return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')   # http://127.0.0.1:5000/store/some_name
def get_store(name):                  # here 'some_name' has to be the 'name'
  # iterate over stores
  # return the name when matches
  # if none matches, return error message
  for store in stores:
    if store['name'] == name:
      return jsonify(store)
    else:
      return jsonify({"messege":"Store not found!"})

# GET /store
@app.route('/store')
def get_stores():
  return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()
  for store in stores:
    if store["name"] == name:
      new_item = {
          "name": request_data["name"],
          "price": request_data["price"]
      }
      store['items'].append(new_item)
      return jsonify(new_item)

  return jsonify({"messege": "Store not found"})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_from_store(name):
  for store in stores:
    if store['name'] == name:
      return jsonify({"items":store['items']})
  
  return jsonify({"messege": "Store not found"})

# run the app in specified folder
app.run(port=5000)