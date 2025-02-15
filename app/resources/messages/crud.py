import uuid
from sqlalchemy.orm import Session
from app.resources.messages.model import Message
from app.resources.messages.schemas import SendMessageRequest
from app.resources.init_config.model import InitConfig  # Import prime & generator
from app.resources.public_keys.model import ServerIdentity  # Import private key
from app.resources.messages.utils import generate_schnorr_proof

def get_prime_and_generator(db: Session):
    """Fetch the prime and generator values from the database."""
    config = db.query(InitConfig).first()
    if not config:
        raise ValueError("Prime and generator have not been initialized.")
    return config.prime, config.generator

def get_private_key(db: Session, server_id: str):
    """
    Fetch the private key of the given server ID.
    If no private key is found, return an appropriate error.
    """
    identity = db.query(ServerIdentity).filter(ServerIdentity.server_id == server_id).first()
    if not identity:
        raise ValueError(f"Server identity not found for server: {server_id}")
    if identity.private_key is None:
        raise ValueError(f"Private key missing for server: {server_id}")
    return identity.private_key

def store_message(db: Session, request: SendMessageRequest):
    """Stores an encrypted message with the sender's ID and generates Schnorr proof."""
    prime, generator = get_prime_and_generator(db)
    private_key = get_private_key(db, request.server_id)

    # Generate Schnorr proof
    commitment, proof, challenge = generate_schnorr_proof(
        request.message, private_key, prime, generator
    )

    # ✅ Convert large integers to strings before storing
    db_message = Message(
        id=str(uuid.uuid4()),  # Store as UUID
        server_id=request.server_id,
        message=request.message,
        commitment=str(commitment),  # Store as string
        proof=str(proof),  # Store as string
        challenge=str(challenge),  # Store as string
    )
    db.add(db_message)
    db.commit()
    return db_message

def get_message(db: Session, server_id: str):
    """Retrieves the last message sent by a specific server."""
    msg = (
        db.query(Message)
        .filter(Message.server_id == server_id)
        .order_by(Message.timestamp.desc())
        .first()
    )

    if msg:
        print(f"🛠 Retrieved -> Commitment: {msg.commitment}, Proof: {msg.proof}, Challenge: {msg.challenge}")
        return msg  # ✅ Return the ORM object, not a dictionary

    return None

