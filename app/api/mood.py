from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.database.models import User, MoodEntry


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if request.energy < 1 or request.energy > 10:
        raise HTTPException(
            status_code=400,
            detail="Energy must be between 1 and 10."
        )

    allowed_moods = {
        "joyful",
        "content",
        "neutral",
        "anxious",
        "sad"
    }

    if request.mood not in allowed_moods:
        raise HTTPException(
            status_code=400,
            detail="Invalid mood."
        )

    mood_entry = MoodEntry(
        user_id=current_user.id,
        mood=request.mood,
        energy=request.energy
    )

    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)

    return {
        "message": "Mood saved successfully.",
        "id": mood_entry.id,
        "mood": mood_entry.mood,
        "energy": mood_entry.energy,
        "created_at": mood_entry.created_at
    }


@router.get("/history")
def mood_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entries = (
        db.query(MoodEntry)
        .filter(
            MoodEntry.user_id == current_user.id
        )
        .order_by(
            MoodEntry.created_at.desc()
        )
        .limit(30)
        .all()
    )

    return {
        "user_id": current_user.id,
        "history": [
            {
                "id": entry.id,
                "mood": entry.mood,
                "energy": entry.energy,
                "date": entry.created_at.isoformat()
            }
            for entry in entries
        ]
    }