from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

class Settings(BaseSettings):
    """Application configuration settings."""
    
    APP_NAME: str = "FastAPI ZKP"
    VERSION: str = "0.1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/db.sqlite3")

    class Config:
        env_file = ".env"

settings = Settings()
