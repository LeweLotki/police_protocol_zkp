from sqlalchemy import Column, String, ForeignKey, DateTime, func
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)  # UUID primary key
    server_id = Column(String, ForeignKey("public_keys.server_id"), nullable=False)
    message = Column(String, nullable=False)
    commitment = Column(String, nullable=False)  # ✅ Store large numbers as strings
    proof = Column(String, nullable=False)  # ✅ Store large numbers as strings
    challenge = Column(String, nullable=False)  # ✅ Store large numbers as strings
    timestamp = Column(DateTime, default=func.now(), nullable=False)  # ✅ Timestamp added

