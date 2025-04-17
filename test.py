import json
import pytest
from application import application as app, db
from models import Blacklist  
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_headers():
    access_token = create_access_token(identity="testuser")
    return {"Authorization": f"Bearer {access_token}"}

def test_post_blacklist_success(client, auth_headers):
    payload = {
        "email": "spam@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "Test reason"
    }

    response = client.post("/blacklists", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == payload["email"]
    assert data["blocked_reason"] == payload["blocked_reason"]


def test_get_blacklist_found(client, auth_headers):
    
    entry = Blacklist(
        email="found@example.com",
        app_uuid="abc",
        blocked_reason="Test",
        ip_address="127.0.0.1"
    )
    db.session.add(entry)
    db.session.commit()

    response = client.get("/blacklists/found@example.com", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_blacklisted"] is True
    assert data["blocked_reason"] == "Test"

def test_get_blacklist_not_found(client, auth_headers):
    response = client.get("/blacklists/notfound@example.com", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()["is_blacklisted"] is False
