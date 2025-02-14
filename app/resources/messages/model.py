from sqlalchemy import Column, String, Integer, DateTime, func
from app.core.database import Base

class Message(Base):
    """Database model for storing encrypted messages and sender IDs."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    server_id = Column(String, index=True)  # The sender's unique ID
    message = Column(String, nullable=False)  # The encrypted message
    proof = Column(String, nullable=True)  # Placeholder for Schnorr proof
    timestamp = Column(DateTime, default=func.now())  # Timestamp of the message

