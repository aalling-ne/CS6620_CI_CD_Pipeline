import pytest
import requests

BASE_URL = "http://flask-api:5000"

@pytest.fixture
def example_item():
    return {'id': '1', 'name': 'Test Item'}

def test_post_item(example_item):
    response = requests.post(f'{BASE_URL}/api/items', json=example_item)
    assert response.status_code == 201

def test_get_all_items(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.get(f"{BASE_URL}/api/items")
    assert response.status_code == 200

def test_get_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.get(f"{BASE_URL}/api/items/{example_item['id']}")
    assert response.status_code == 200
    assert response.json() == example_item

def test_update_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)

    updated_item = {'id': '1', 'favorite_color': 'green'}

    response = requests.put(f"{BASE_URL}/api/items/{example_item['id']}", json = updated_item)
    assert response.status_code == 200
    assert response.json() == updated_item

def test_delete_single_item(example_item):
    requests.post(f"{BASE_URL}/api/items", json=example_item)
    response = requests.delete(f"{BASE_URL}/api/items/1")
    assert response.status_code == 204

def test_bad_request_get():
    response = requests.get(f"{BASE_URL}/api/items/thisItemDoesntExist")
    assert response.status_code == 404