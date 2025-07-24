# CS6620 Summer 2025
# CI/CD Pipeline Part 2 - Dockerized REST API
# Alexander Alling

from flask import Flask, jsonify, request, abort
import boto3
from botocore.exceptions import ClientError
import os
import json


app = Flask(__name__)

app_dictionary = {}

# SET UP AWS

# initialize s3
s3 = boto3.client(
    "s3",
    endpoint_url = os.environ.get("S3_ENDPOINT_URL"),
    region_name = os.environ.get("AWS_REGION"),
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

def create_s3_bucket():
    try:
        s3.create_bucket(Bucket="s3bucket")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Bucket already created.")
        else:
            raise

# initialize dynamodb

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL"),
    region_name = os.environ.get("AWS_REGION"),
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)

def create_dynamodb_table():
    try:
        dynamodb.create_table(
            TableName="dynamodb_table",
            KeySchema=[{"AttributeName":"id", "KeyType": "HASH"}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            print("Table already created.")
        else:
            raise

# initialize s3 bucket and db table
create_s3_bucket()
create_dynamodb_table()

# S3 Helper Functions
def copy_to_s3(item):
    s3.put_object(Bucket="s3bucket", Key=item["id"], Body=json.dumps(item))

def delete_from_s3(item_id):
    s3.delete_object(Bucket="s3bucket", Key=item_id)

# DynamoDB Helper Functions
def copy_to_dynamodb(item):
    dynamodb.Table("dynamodb_table").put_item(Item=item)

def delete_from_dynamodb(item_id):
    dynamodb.Table("dynamodb_table").delete_item(Key={"id": item_id})

# APP ROUTES ---------------------------------

# POST METHODS

@app.route("/api/items", methods=['POST'])
def create_item():
    item = request.get_json()
    if (not item) or ("id" not in item):
        abort(400, "Post requests must be made with the following format: {'id': 'example_id', ...other key-value pairs...}")
    if item['id'] in app_dictionary:
        abort(400, "Item with that id already in database. POST not accepted.")
    app_dictionary[item['id']] = item
    copy_to_dynamodb(item)
    copy_to_s3(item)
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
    copy_to_dynamodb(item)
    copy_to_s3(item)
    return item, 200

# DELETE METHODS

@app.route("/api/items/<string:item_id>", methods=["DELETE"])
def delete_single_item(item_id):
    if (item_id not in app_dictionary):
        abort(404, "The item_id you are trying to delete does not exist.")
    del app_dictionary[item_id]
    delete_from_dynamodb(item_id)
    delete_from_s3(item_id)
    return "Success", 204

# HEALTH CHECKER
@app.route('/health')
def health():
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
