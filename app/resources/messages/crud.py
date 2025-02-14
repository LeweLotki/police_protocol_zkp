from sqlalchemy.orm import Session
from app.resources.messages.model import Message
from app.resources.messages.schemas import SendMessageRequest

def store_message(db: Session, request: SendMessageRequest):
    """Stores an encrypted message with the sender's ID."""
    db_message = Message(
        server_id=request.server_id,
        message=request.message,
        proof="MOCK_PROOF"  # Placeholder for Schnorr proof
    )
    db.add(db_message)
    db.commit()
    return db_message

def get_message(db: Session, server_id: str):
    """Retrieves the last message sent by a specific server."""
    return db.query(Message).filter(Message.server_id == server_id).order_by(Message.timestamp.desc()).first()

