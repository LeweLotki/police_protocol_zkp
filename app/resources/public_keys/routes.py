from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.core.database import get_db
from app.resources.public_keys import crud, schemas, utils

router = APIRouter()

# Server's unique ID (set when the server starts)
SERVER_ID = str(uuid.uuid4())

@router.post("/calculate", response_model=schemas.PublicKeyCalculationResponse)
def calculate_public_key(request: schemas.PublicKeyCalculationRequest):
    """
    Endpoint to calculate public key from private key.
    """
    private_key = utils.generate_private_key(request.prime)
    public_key = utils.compute_public_key(request.generator, private_key, request.prime)
    return {"public_key": public_key, "private_key": private_key}

@router.post("/send", response_model=dict)
def send_public_key(public_key_data: schemas.PublicKeyCreate, db: Session = Depends(get_db)):
    """
    Endpoint to store public key along with the server's UUID.
    """
    stored_key = crud.store_public_key(db, public_key_data)
    return {"message": "Public key stored successfully"}

@router.get("/{server_id}", response_model=schemas.PublicKeyResponse)
def get_public_key(server_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a stored public key by server ID.
    """
    public_key = crud.get_public_key(db, server_id)
    
    if not public_key:
        raise HTTPException(status_code=404, detail="Public key not found")

    return {"server_id": public_key.server_id, "public_key": public_key.public_key}

