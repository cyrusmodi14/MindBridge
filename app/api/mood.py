from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.database.models import User

router = APIRouter(
    prefix="/mood",
    tags=["Mood"]
)


class MoodRequest(BaseModel):
    mood: str
    energy: int


@router.post("/")
def save_mood(
    request: MoodRequest,
    current_user: User = Depends(get_current_user)
):
    # For now, this only returns the submitted data.
    # Later we'll save it to PostgreSQL.

    return {
        "message": "Mood saved",
        "mood": request.mood,
        "energy": request.energy
    }


@router.get("/history")
def mood_history(
    current_user: User = Depends(get_current_user)
):
    return {
        "history": []
    }