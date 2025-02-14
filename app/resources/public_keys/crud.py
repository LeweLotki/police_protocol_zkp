from sqlalchemy.orm import Session
from app.resources.public_keys.model import PublicKey, ServerIdentity
from app.resources.public_keys.schemas import PublicKeyCreate
from app.resources.public_keys.utils import generate_private_key, compute_public_key

def store_server_identity(db: Session, prime: int, generator: int, server_id: str):
    """Stores the private and public key for this server."""
    private_key = generate_private_key(prime)
    public_key = compute_public_key(generator, private_key, prime)

    db_server = ServerIdentity(
        server_id=server_id,
        private_key=private_key,
        public_key=public_key
    )
    db.add(db_server)
    db.commit()
    return db_server

def get_server_identity(db: Session, server_id: str):
    """Retrieves the server's private & public key (used internally)."""
    return db.query(ServerIdentity).filter(ServerIdentity.server_id == server_id).first()

def store_public_key(db: Session, public_key_data: PublicKeyCreate):
    """Stores a public key and server ID from an external client."""
    existing_key = db.query(PublicKey).filter(PublicKey.server_id == public_key_data.server_id).first()

    if existing_key:
        existing_key.public_key = public_key_data.public_key  # Update existing key
    else:
        db_public_key = PublicKey(
            server_id=public_key_data.server_id,
            public_key=public_key_data.public_key
        )
        db.add(db_public_key)

    db.commit()
    return existing_key if existing_key else db_public_key

def get_public_key(db: Session, server_id: str):
    """Retrieves a public key by server ID."""
    return db.query(PublicKey).filter(PublicKey.server_id == server_id).first()

