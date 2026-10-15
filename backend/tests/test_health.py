import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test that /api/health returns 200 OK and expected structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "UP"
    assert "database" in json_data["data"]

def test_404_error_handler(client):
    """Test that undefined routes return standardized 404 JSON."""
    response = client.get("/api/non-existent-route")
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "not found" in json_data["message"].lower()

