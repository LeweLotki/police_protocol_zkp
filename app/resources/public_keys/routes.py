from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.core.database import get_db
from app.resources.public_keys import crud, schemas, utils

router = APIRouter()

# Unique ID for this server (created once on startup)
SERVER_ID = str(uuid.uuid4())

@router.post("/calculate", response_model=schemas.PublicKeyCalculationResponse)
def calculate_public_key(request: schemas.PublicKeyCalculationRequest):
    """
    Computes a public key from a private key.
    """
    private_key = utils.generate_private_key(request.prime)
    public_key = utils.compute_public_key(request.generator, private_key, request.prime)
    return {"public_key": public_key, "private_key": private_key}

@router.post("/initialize", response_model=schemas.PublicKeyResponse)
def initialize_server_keys(request: schemas.PublicKeyCalculationRequest, db: Session = Depends(get_db)):
    """
    Initializes this server's private and public key based on a prime and generator.
    This should be called once when the server starts.
    """
    existing_identity = crud.get_server_identity(db, SERVER_ID)
    if existing_identity:
        raise HTTPException(status_code=400, detail="Server keys already initialized")

    server_identity = crud.store_server_identity(db, request.prime, request.generator, SERVER_ID)
    return {"server_id": server_identity.server_id, "public_key": server_identity.public_key}

@router.get("/my_public_key", response_model=schemas.PublicKeyResponse)
def get_my_public_key(db: Session = Depends(get_db)):
    """
    Retrieves the public key of this server.
    """
    identity = crud.get_server_identity(db, SERVER_ID)
    if not identity:
        raise HTTPException(status_code=404, detail="Server identity not found")

    return {"server_id": identity.server_id, "public_key": identity.public_key}

@router.post("/send", response_model=dict)
def send_public_key(public_key_data: schemas.PublicKeyCreate, db: Session = Depends(get_db)):
    """
    Endpoint to store a public key received from another server in the network.
    """
    stored_key = crud.store_public_key(db, public_key_data)
    return {"message": "Public key stored successfully"}

@router.get("/{server_id}", response_model=schemas.PublicKeyResponse)
def get_public_key(server_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the public key of another server by its ID.
    """
    public_key = crud.get_public_key(db, server_id)
    
    if not public_key:
        raise HTTPException(status_code=404, detail="Public key not found")

    return {"server_id": public_key.server_id, "public_key": public_key.public_key}

