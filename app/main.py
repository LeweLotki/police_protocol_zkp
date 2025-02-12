from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base

from app.resources.init_config.routes import router as init_config_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A FastAPI implementation of a Zero-Knowledge Proof protocol"
)

Base.metadata.create_all(bind=engine)

app.include_router(init_config_router, prefix="/initial_configuration", tags=["Init Config"])
