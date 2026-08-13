from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered mental health support and therapist bridge",
    version=settings.APP_VERSION
)


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