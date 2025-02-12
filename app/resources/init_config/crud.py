from sqlalchemy.orm import Session
from app.resources.init_config.model import InitConfig
from app.resources.init_config.schemas import InitConfigCreate

def set_initial_configuration(db: Session, config: InitConfigCreate):
    """Stores the prime number and generator in the database."""
    db.query(InitConfig).delete() 
    
    db_config = InitConfig(prime=config.prime, generator=config.generator)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    return db_config

def get_initial_configuration(db: Session):
    """Retrieves the stored prime number and generator."""
    config = db.query(InitConfig).order_by(InitConfig.id.desc()).first()

    if not config:
        return None 

    return config

