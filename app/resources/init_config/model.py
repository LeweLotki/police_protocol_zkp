from sqlalchemy import Column, Integer
from app.core.database import Base

class InitConfig(Base):
    """Database model for storing the prime and generator used in ZKP."""
    __tablename__ = "init_config"

    id = Column(Integer, primary_key=True, index=True)
    prime = Column(Integer, nullable=False)
    generator = Column(Integer, nullable=False)

