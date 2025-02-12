from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.resources.init_config import crud, schemas, utils

router = APIRouter()

@router.post("/", response_model=schemas.InitConfigResponse)
def set_initial_configuration(config: schemas.InitConfigCreate, db: Session = Depends(get_db)):
    """
    Endpoint to store a prime number and generator.
    """
    if not utils.is_prime(config.prime):
        raise HTTPException(status_code=400, detail="Invalid prime number. Must be a prime.")

    if not utils.is_valid_generator(config.generator, config.prime):
        raise HTTPException(status_code=400, detail="Invalid generator for the given prime.")

    stored_config = crud.set_initial_configuration(db, config)

    return {
        "prime": stored_config.prime,
        "generator": stored_config.generator,
        "message": "Prime and generator set successfully"
    }

@router.get("/", response_model=schemas.InitConfigResponse)
def get_initial_configuration(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the stored prime number and generator.
    """
    config = crud.get_initial_configuration(db)

    if not config:
        raise HTTPException(status_code=404, detail="No configuration found")

    return {"prime": config.prime, "generator": config.generator}

