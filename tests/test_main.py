from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to FastAPI Service",
        "status": "healthy",
    }


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "fastapi-service"}


def test_create_item():
    """Test creating a new item"""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 29.99,
        "tax": 2.99,
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 29.99
    assert "id" in data


def test_read_items():
    """Test reading items list"""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_item():
    """Test reading a specific item"""
    # First create an item
    item_data = {
        "name": "Specific Item",
        "description": "A specific test item",
        "price": 19.99,
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Then read it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Specific Item"
    assert data["id"] == item_id


def test_delete_item():
    """Test deleting an item"""
    # First create an item
    item_data = {"name": "Delete Me", "price": 9.99}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Item {item_id} deleted"}

    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Item not found"}


def test_read_nonexistent_item():
    """Test reading a non-existent item"""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_nonexistent_item():
    """Test deleting a non-existent item"""
    response = client.delete("/items/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
