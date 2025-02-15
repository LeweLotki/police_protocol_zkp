# tests/test_messages.py
from app.core.database import get_db
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
    """Setup server keys for testing, ensuring private keys are stored correctly."""
    from app.core.database import get_db
    from app.resources.public_keys.model import ServerIdentity

    # Initialize prime and generator
    client.post("/public_keys/initialize", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})

    # Generate key pair for TEST_SERVER_ID_1
    response_1 = client.post("/public_keys/calculate", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    private_key_1 = response_1.json()["private_key"]
    public_key_1 = response_1.json()["public_key"]
    client.post("/public_keys/send", json={"server_id": TEST_SERVER_ID_1, "public_key": public_key_1})

    # Generate key pair for TEST_SERVER_ID_2
    response_2 = client.post("/public_keys/calculate", json={"prime": VALID_PRIME, "generator": VALID_GENERATOR})
    private_key_2 = response_2.json()["private_key"]
    public_key_2 = response_2.json()["public_key"]
    client.post("/public_keys/send", json={"server_id": TEST_SERVER_ID_2, "public_key": public_key_2})

    # Store private keys in the database
    db = next(get_db())  # Get a database session
    db.add(ServerIdentity(server_id=TEST_SERVER_ID_1, public_key=public_key_1, private_key=private_key_1))
    db.add(ServerIdentity(server_id=TEST_SERVER_ID_2, public_key=public_key_2, private_key=private_key_2))
    db.commit()

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

