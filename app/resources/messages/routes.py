from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.resources.messages import crud, schemas, utils
from app.resources.public_keys.model import ServerIdentity
from app.resources.init_config.model import InitConfig

router = APIRouter()

@router.post("/send", response_model=schemas.SendMessageResponse)
def send_message(request: schemas.SendMessageRequest, db: Session = Depends(get_db)):
    """
    Receives an encrypted message, generates a Schnorr proof, and stores it.
    """
    stored_message = crud.store_message(db, request)
    return {"message": "Message sent successfully"}

@router.post("/verify", response_model=schemas.VerifyMessageResponse)
def verify_message(request: schemas.VerifyMessageRequest, db: Session = Depends(get_db)):
    """
    Verifies the Schnorr proof for a received message.
    """
    stored_message = crud.get_message(db, request.server_id)
    if not stored_message:
        raise HTTPException(status_code=404, detail="No message found for this server ID.")

    # Fetch prime, generator, and public key of the sender
    config = db.query(InitConfig).first()
    if not config:
        raise HTTPException(status_code=500, detail="Prime and generator are not initialized.")

    prime, generator = config.prime, config.generator

    sender_identity = db.query(ServerIdentity).filter(ServerIdentity.server_id == request.server_id).first()
    if not sender_identity:
        raise HTTPException(status_code=404, detail="Public key not found for sender.")

    public_key = sender_identity.public_key

    # Verify Schnorr proof
    is_valid = utils.verify_schnorr_proof(
        message=request.message,
        commitment=stored_message.proof,  # In a real implementation, commitment should be stored separately
        proof=stored_message.proof,  # Use the stored proof
        challenge=utils.hash_value(stored_message.message),  # Recompute challenge
        public_key=public_key,
        prime=prime,
        generator=generator
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail="Message verification failed")

    return {"message": "Message verified successfully"}

