from sqlalchemy import Column, String, Integer
from app.core.database import Base

class ServerIdentity(Base):
    """
    Stores our own server identity:
    - Private key (not exposed via API)
    - Public key
    - Server UUID
    """
    __tablename__ = "server_identity"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String, unique=True, nullable=False, index=True)
    private_key = Column(Integer, nullable=False)  # Only used internally
    public_key = Column(Integer, nullable=False)

class PublicKey(Base):
    """
    Stores public keys of other clients in the network.
    - Each client has a UUID and a public key.
    """
    __tablename__ = "public_keys"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String, unique=True, nullable=False, index=True)
    public_key = Column(Integer, nullable=False)

