import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app_context():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_context):
    return app_context.test_client()

def test_register_user_success(client):
    """Test successful user registration returns 201 and JWT access token."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    res = response.get_json()
    assert res["success"] is True
    assert "access_token" in res["data"]
    assert res["data"]["user"]["email"] == "jane@example.com"
    assert "password_hash" not in res["data"]["user"]

def test_register_duplicate_email(client):
    """Test duplicate registration returns 409 Conflict."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "SecurePassword123!"
    }
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409
    res = response.get_json()
    assert res["success"] is False
    assert "already exists" in res["message"]

def test_register_short_password(client):
    """Test password under 8 characters is rejected."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "short"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    res = response.get_json()
    assert res["success"] is False

def test_login_success(client):
    """Test login with valid credentials returns 200 and access token."""
    # Register first
    client.post("/api/auth/register", json={
        "full_name": "John Smith",
        "email": "john@example.com",
        "password": "ValidPassword99!"
    })

    # Login
    response = client.post("/api/auth/login", json={
        "email": "john@example.com",
        "password": "ValidPassword99!"
    })
    assert response.status_code == 200
    res = response.get_json()
    assert res["success"] is True
    assert "access_token" in res["data"]
    assert res["data"]["user"]["email"] == "john@example.com"

def test_login_invalid_password(client):
    """Test login with incorrect password returns 401 Unauthorized."""
    client.post("/api/auth/register", json={
        "full_name": "John Smith",
        "email": "john@example.com",
        "password": "ValidPassword99!"
    })

    response = client.post("/api/auth/login", json={
        "email": "john@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    res = response.get_json()
    assert res["success"] is False

def test_protected_user_profile(client):
    """Test GET /api/users/me with JWT Bearer token."""
    reg = client.post("/api/auth/register", json={
        "full_name": "Alex Rivera",
        "email": "alex@example.com",
        "password": "MySecretPassword88!"
    })
    token = reg.get_json()["data"]["access_token"]

    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    res = response.get_json()
    assert res["success"] is True
    assert res["data"]["full_name"] == "Alex Rivera"

def test_unauthorized_user_profile(client):
    """Test GET /api/users/me without Bearer token returns 401."""
    response = client.get("/api/users/me")
    assert response.status_code == 401
