from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.resources.messages import crud, schemas, utils

router = APIRouter()

@router.post("/send", response_model=schemas.SendMessageResponse)
def send_message(request: schemas.SendMessageRequest, db: Session = Depends(get_db)):
    """
    Receives an encrypted message and stores it in the database.
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

    if not utils.verify_schnorr_proof(request.message, stored_message.proof):
        raise HTTPException(status_code=400, detail="Message verification failed")

    return {"message": "Message verified successfully"}

