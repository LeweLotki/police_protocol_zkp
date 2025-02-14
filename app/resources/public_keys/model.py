from sqlalchemy import Column, String, Integer
from app.core.database import Base

class PublicKey(Base):
    """Database model for storing public keys of both self and other clients."""
    __tablename__ = "public_keys"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String, unique=True, nullable=False, index=True)
    public_key = Column(Integer, nullable=False)

