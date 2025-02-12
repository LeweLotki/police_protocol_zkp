# tests/test_init_config.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Sample test values
VALID_PRIME = 23  # Replace with a proper large prime in production
VALID_GENERATOR = 5

INVALID_PRIME = 21  # Composite number (not a prime)
INVALID_GENERATOR = 10  # Not a valid generator for the group

# Test successful transaction of sharing prime and generator
def test_share_valid_prime_and_generator():
    response = client.post("/initial_configuration", json={
        "prime": VALID_PRIME,
        "generator": VALID_GENERATOR
    })
    assert response.status_code == 200
    assert response.json() == {
        "prime": VALID_PRIME,
        "generator": VALID_GENERATOR,
        "message": "Prime and generator set successfully"
    }

# Test that prime must be an actual prime number
def test_reject_invalid_prime():
    response = client.post("/initial_configuration", json={
        "prime": INVALID_PRIME,
        "generator": VALID_GENERATOR
    })
    assert response.status_code == 400
    assert "Invalid prime number" in response.json()["detail"]

# Test that generator must be valid
def test_reject_invalid_generator():
    response = client.post("/initial_configuration", json={
        "prime": VALID_PRIME,
        "generator": INVALID_GENERATOR
    })
    assert response.status_code == 400
    assert "Invalid generator" in response.json()["detail"]

# Test fetching the current stored configuration
def test_get_current_configuration():
    # First, store a valid prime and generator
    client.post("/initial_configuration", json={
        "prime": VALID_PRIME,
        "generator": VALID_GENERATOR
    })

    # Then, retrieve it
    response = client.get("/initial_configuration")
    assert response.status_code == 200
    assert response.json() == {
        "prime": VALID_PRIME,
        "generator": VALID_GENERATOR
    }

