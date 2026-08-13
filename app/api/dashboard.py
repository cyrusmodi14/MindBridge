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
    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user.id
        )
        .order_by(
            Assessment.created_at.desc()
        )
        .all()
    )

    latest = assessments[0] if assessments else None

    if latest is None:
        return {
            "user_name": current_user.email.split("@")[0],
            "current_vibe": "No assessment yet",
            "overall_score": None,
            "category": None,
            "assessment_id": None,
            "latest_insight": (
                "Complete your first wellness assessment "
                "to begin building your Solace insights."
            ),
            "weekly_activity": []
        }

    category = latest.category

    if isinstance(category, dict):
        current_vibe = (
            category.get("label")
            or category.get("category")
            or "Assessment complete"
        )
    else:
        current_vibe = str(category)

    weekly_activity = [
        {
            "assessment_id": assessment.id,
            "score": assessment.overall_score,
            "date": assessment.created_at.isoformat()
        }
        for assessment in assessments[:7]
    ]

    return {
        "user_name": current_user.email.split("@")[0],
        "current_vibe": current_vibe,
        "overall_score": latest.overall_score,
        "category": category,
        "assessment_id": latest.id,
        "latest_insight": (
            "Your latest assessment has been recorded. "
            "Continue checking in to build a clearer picture "
            "of your emotional wellbeing."
        ),
        "weekly_activity": weekly_activity
    }