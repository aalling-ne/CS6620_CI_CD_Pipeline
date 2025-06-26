# CS6620 Summer 2025
# CI/CD Pipeline Part 2 - Dockerized REST API
# Alexander Alling

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

app_dictionary = {}

# POST METHODS

@app.route("/api/items", methods=['POST'])
def create_item():
    item = request.get_json()
    if (not item) or ("id" not in item):
        abort(400, "Post requests must be made with the following format: {'id': 'example_id', ...other key-value pairs...}")
    app_dictionary[item['id']] = item
    return item, 201

# GET METHODS

@app.route("/api/items", methods=["GET"])
def get_items():
    return app_dictionary, 200

@app.route("/api/items/<string:item_id>", methods=["GET"])
def get_single_item(item_id):
    item = app_dictionary.get(item_id)
    if (not item):
        abort(404, "The item_id you are looking for does not exist.")
    return item, 200

# PUT METHODS

@app.route("/api/items/<string:item_id>", methods=["PUT"])
def update_single_item(item_id):
    item = request.get_json()
    if (item_id not in app_dictionary):
        abort(404, "The item_id you are trying to modify does not exist.")
    app_dictionary[item_id] = item
    return item, 200

# DELETE METHODS

@app.route("/api/items/<string:item_id>", methods=["DELETE"])
def delete_single_item(item_id):
    if (item_id not in app_dictionary):
        abort(404, "The item_id you are trying to delete does not exist.")
    del app_dictionary[item_id]
    return "Success", 204

# HEALTH CHECKER
@app.route('/health')
def health():
    return "ok", 200


