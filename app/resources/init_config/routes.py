from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.resources.init_config import crud, schemas

router = APIRouter()

@router.post("/")
def set_initial_configuration(config: schemas.InitConfigCreate, db: Session = Depends(get_db)):
    """
    Endpoint to store a prime number and generator.
    """
    # TODO: Implement logic to store the prime and generator
    return {"message": "Endpoint not yet implemented"}

@router.get("/")
def get_initial_configuration(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the stored prime number and generator.
    """
    # TODO: Implement logic to retrieve the prime and generator
    return {"message": "Endpoint not yet implemented"}

