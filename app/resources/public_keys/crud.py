from sqlalchemy.orm import Session
from app.resources.public_keys.model import PublicKey
from app.resources.public_keys.schemas import PublicKeyCreate

def store_public_key(db: Session, public_key_data: PublicKeyCreate):
    """Stores or updates a public key for a server."""
    existing_key = db.query(PublicKey).filter(PublicKey.server_id == public_key_data.server_id).first()

    if existing_key:
        existing_key.public_key = public_key_data.public_key
    else:
        db_public_key = PublicKey(
            server_id=public_key_data.server_id,
            public_key=public_key_data.public_key
        )
        db.add(db_public_key)

    db.commit()
    return existing_key if existing_key else db_public_key

def get_public_key(db: Session, server_id: str):
    """Retrieves a stored public key by server ID."""
    return db.query(PublicKey).filter(PublicKey.server_id == server_id).first()

