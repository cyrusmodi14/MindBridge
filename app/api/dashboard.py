from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.database.models import User, Assessment

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    latest = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user.id
        )
        .order_by(
            Assessment.created_at.desc()
        )
        .first()
    )

    if latest is None:

        return {
            "user_name": current_user.email.split("@")[0],
            "current_vibe": "No check-in yet",
            "overall_score": None,
            "latest_insight": None
        }


    return {
        "user_name": current_user.email.split("@")[0],
        "current_vibe": latest.category,
        "overall_score": latest.overall_score,
        "latest_insight": None
    }