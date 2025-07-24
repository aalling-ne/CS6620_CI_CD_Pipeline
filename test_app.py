import pytest
import requests
import os
import boto3
from botocore.exceptions import ClientError
import json
import time

# BASE_URL is set in docker-compose.test.yml, or defaults to localhost if tests are ran without using Docker Compose
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

# AWS Connections
s3 = boto3.client(
    "s3",
    endpoint_url = os.environ.get("S3_ENDPOINT_URL"),
    region_name = os.environ.get("AWS_REGION"),
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL"),
    region_name = os.environ.get("AWS_REGION"),
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)

@pytest.fixture
def example_item():
    return {'id': '1', 'name': 'Test Item'}

# Helper Functions
def get_item_from_dynamodb(item_id):
    return dynamodb.Table("dynamodb_table").get_item(Key={"id": item_id}).get("Item")

def get_item_from_s3(item_id):
    response = s3.get_object(Bucket="s3bucket", Key=f"{item_id}.json")
    return json.loads(response['Body'].read())

# Tests

# GET
def test_get_all_items(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.get(f"{BASE_URL}/api/items")
    assert response.status_code == 200

def test_get_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.get(f"{BASE_URL}/api/items/{example_item['id']}")
    assert response.status_code == 200
    assert response.json() == example_item

    time.sleep(1)
    assert get_item_from_dynamodb(example_item["id"]) == example_item
    assert get_item_from_s3(example_item["id"]) == example_item

def test_get_bad_request():
    response = requests.get(f"{BASE_URL}/api/items/thisItemDoesntExist")
    assert response.status_code == 404

# POST
def test_post_item(example_item):
    response = requests.post(f'{BASE_URL}/api/items', json=example_item)
    assert response.status_code == 201

    time.sleep(1)
    assert get_item_from_dynamodb(example_item["id"]) == example_item
    assert get_item_from_s3(example_item["id"]) == example_item

def test_duplicate_post(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    duplicate = requests.post(f"{BASE_URL}/api/items", json=example_item)
    assert duplicate.status_code == 400

# PUT
def test_update_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    time.sleep(1)

    updated_item = {'id': '1', 'favorite_color': 'green'}
    response = requests.put(f"{BASE_URL}/api/items/{example_item['id']}", json = updated_item)
    assert response.status_code == 200
    assert response.json() == updated_item

    time.sleep(1)
    assert get_item_from_dynamodb(example_item["id"]) == updated_item
    assert get_item_from_s3(example_item["id"]) == updated_item

def test_put_bad_request():
    update = {'id': 'doesnotexist', 'favorite_color': 'octarine'}
    response = requests.put(f"{BASE_URL}/api/items/doesnotexist", json=update)
    assert response.status_code == 404

# DELETE
def test_delete_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.delete(f"{BASE_URL}/api/items/1")
    assert response.status_code == 204

    time.sleep(1)

    assert get_item_from_dynamodb(example_item["id"]) is None
    assert get_item_from_s3(example_item["id"]) is None
