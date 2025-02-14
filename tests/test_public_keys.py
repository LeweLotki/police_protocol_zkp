# tests/test_public_keys.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

# Sample prime number for key derivation
VALID_PRIME = 23  # Replace with a secure prime in production
VALID_GENERATOR = 5

INVALID_PRIME = 21  # Composite number (not a prime)

# Generate a UUID for testing
TEST_SERVER_ID = str(uuid.uuid4())

# Test public key calculation from private key
def test_calculate_public_key():
    response = client.post("/public_keys/calculate", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    assert response.status_code == 200
    data = response.json()
    
    assert "public_key" in data
    assert "private_key" in data  # For testing, we return this, but it won't be stored

# Test storing a public key with server ID
def test_store_public_key():
    response = client.post("/public_keys/send", json={
        "server_id": TEST_SERVER_ID,
        "public_key": 10  # Example public key
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Public key stored successfully"}

# Test retrieving a stored public key
def test_get_public_key():
    # First, store a public key
    client.post("/public_keys/send", json={
        "server_id": TEST_SERVER_ID,
        "public_key": 10
    })

    # Then, retrieve it
    response = client.get(f"/public_keys/{TEST_SERVER_ID}")
    assert response.status_code == 200
    assert response.json() == {
        "server_id": TEST_SERVER_ID,
        "public_key": 10
    }

# Test retrieving a non-existent public key
def test_get_nonexistent_public_key():
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/public_keys/{random_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Public key not found"}

# Test initializing the server's private and public key
def test_initialize_server_keys():
    response = client.post("/public_keys/initialize", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    assert response.status_code == 200
    data = response.json()

    assert "server_id" in data
    assert "public_key" in data

# Test initializing server keys when they already exist
def test_initialize_server_keys_already_exists():
    # First initialization
    client.post("/public_keys/initialize", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})

    # Second initialization attempt (should fail)
    response = client.post("/public_keys/initialize", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    assert response.status_code == 400
    assert response.json()["detail"] == "Server keys already initialized"

# Test retrieving the server's own public key
def test_get_my_public_key():
    response = client.get("/public_keys/my_public_key")
    assert response.status_code == 200
    data = response.json()

    assert "server_id" in data
    assert "public_key" in data

# Test retrieving my public key before initialization (should fail)
# Test retrieving my public key before initialization (should fail)
def test_get_my_public_key_not_initialized():
    """Ensure retrieving my public key before initialization returns 404."""

    # Reset state: Remove any stored keys before running this test
    from app.core.database import SessionLocal
    from app.resources.public_keys.model import ServerIdentity

    db = SessionLocal()
    db.query(ServerIdentity).delete()  # Clear server identity
    db.commit()
    db.close()

    # Now try fetching the public key (should return 404)
    response = client.get("/public_keys/my_public_key")
    assert response.status_code == 404
    assert response.json()["detail"] == "Server identity not found"

