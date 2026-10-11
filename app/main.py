from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.session import engine

# Important: Import all models here so SQLModel registers them before creating tables
from app.models import db_models 

from app.api.endpoints import webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    """
    # Create all tables in the database
    # Note: In a fully mature production app, we would run Alembic migrations here instead
    SQLModel.metadata.create_all(engine)
    yield
    # Resources cleanup can be added here upon shutdown

# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    """
    Simple endpoint to verify the API is running.
    """
    return {"status": "ok", "project": settings.PROJECT_NAME}

app.include_router(webhook.router, prefix="/api/v1", tags=["Telegram"])