# tests/test_messages.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

# Sample data for testing
VALID_PRIME = 23
VALID_GENERATOR = 5
TEST_SERVER_ID_1 = str(uuid.uuid4())
TEST_SERVER_ID_2 = str(uuid.uuid4())
TEST_MESSAGE = "Hello, this is a test message."

def setup_keys():
    """Setup server keys for testing."""
    client.post("/public_keys/initialize", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    client.post("/public_keys/send", json={"server_id": TEST_SERVER_ID_1, "public_key": 10})
    client.post("/public_keys/send", json={"server_id": TEST_SERVER_ID_2, "public_key": 15})

# Test sending a message from a client
def test_send_message():
    setup_keys()
    response = client.post("/messages/send", json={
        "server_id": TEST_SERVER_ID_1,
        "message": TEST_MESSAGE
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent successfully"}

# Test sending a message from another client
def test_send_message_from_another_client():
    response = client.post("/messages/send", json={
        "server_id": TEST_SERVER_ID_2,
        "message": "Another test message"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent successfully"}

# Test verifying a sent message
def test_verify_message():
    # Send a message first
    client.post("/messages/send", json={
        "server_id": TEST_SERVER_ID_1,
        "message": TEST_MESSAGE
    })

    # Verify the message
    response = client.post("/messages/verify", json={
        "server_id": TEST_SERVER_ID_1,
        "message": TEST_MESSAGE
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message verified successfully"}

# Test verifying a message with incorrect details
def test_verify_message_incorrect():
    response = client.post("/messages/verify", json={
        "server_id": TEST_SERVER_ID_1,
        "message": "Incorrect message"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Message verification failed"}

# Test verifying a message from another client
def test_verify_message_from_another_client():
    client.post("/messages/send", json={
        "server_id": TEST_SERVER_ID_2,
        "message": "Another test message"
    })

    response = client.post("/messages/verify", json={
        "server_id": TEST_SERVER_ID_2,
        "message": "Another test message"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Message verified successfully"}

