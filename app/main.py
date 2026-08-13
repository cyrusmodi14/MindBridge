from fastapi import FastAPI

from app.core.config import settings
from app.database.database import Base, engine
from app.database import models
from app.api.auth import router as auth_router

from app.assessment.router import router as assessment_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered mental health support and therapist bridge",
    version=settings.APP_VERSION
)


app.include_router(assessment_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }