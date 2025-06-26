from app import app as flask_app
#note to self, why does "import app as flask_app" not work?

import pytest

#set up app
@pytest.fixture
def app():
    flask_app.testing = True
    with flask_app.test_client() as app:
        yield app

@pytest.fixture
def example_item():
    return {'id': '1', 'name': 'Test Item'}

def test_post_item(app, example_item):
    response = app.post('/api/items', json=example_item)
    assert response.status_code == 201

def test_get_all_items(app, example_item):
    app.post("/api/items", json=example_item)
    response = app.get("/api/items")
    assert response.status_code == 200

def test_get_single_item(app, example_item):
    app.post("/api/items", json=example_item)
    response = app.get(f"/api/items/{example_item["id"]}")
    assert response.status_code == 200
    assert response.get_json() == example_item

def test_update_single_item(app, example_item):
    app.post("/api/items", json=example_item)

    updated_item = {'id': '1', 'favorite_color': 'green'}

    response = app.put(f"/api/items/{example_item["id"]}", json = updated_item)
    assert response.status_code == 200
    assert response.get_json() == updated_item

def test_delete_single_item(app, example_item):
    app.post("/api/items", json=example_item)
    response = app.delete("/api/items/1")
    assert response.status_code == 204

def test_bad_request_get(app):
    response = app.get("api/items/thisItemDoesntExist")
    assert response.status_code == 404