from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.assessment.scoring import calculate_assessment
from app.assessment.safety import check_safety
from app.services.assessment_report import generate_assessment_report

from app.database.database import get_db
from app.database.models import Assessment

from app.core.security import get_current_user


router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


# ============================================================
# REQUEST MODELS
# ============================================================

class AssessmentRequest(BaseModel):

    answers: dict[int, int] = Field(
        ...,
        description="Question ID mapped to answer value from 0 to 4"
    )


class ReassessmentRequest(BaseModel):

    answers: dict[int, int] = Field(
        ...,
        description="Reassessment question ID mapped to answer value from 0 to 4"
    )


# ============================================================
# 1. INITIAL ASSESSMENT SCORE
# ============================================================

@router.post("/score")
def score_assessment(
    request: AssessmentRequest,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Validate answers
    # --------------------------------------------------------

    for question_id, answer in request.answers.items():

        if answer < 0 or answer > 4:

            return {
                "error": (
                    f"Invalid answer for question "
                    f"{question_id}. "
                    "Answer must be between 0 and 4."
                )
            }

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    safety_result = check_safety(request.answers)

    if safety_result["safety_concern"]:

        return {
            "safety_override": True,
            "overall_score": None,
            "category": "safety_concern",
            "safety": safety_result,
            "recommendation": (
                "Please seek immediate support from a "
                "qualified mental-health professional or "
                "appropriate local emergency/crisis services."
            )
        }

    # --------------------------------------------------------
    # Calculate assessment
    # --------------------------------------------------------

    result = calculate_assessment(
        request.answers
    )

    # --------------------------------------------------------
    # Save assessment to database
    # --------------------------------------------------------

    assessment = Assessment(
        user_id=current_user,
        overall_score=result["overall_score"],
        category=result["category"],
        domain_scores=result["domain_scores"],
        answers=request.answers
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "assessment_id": assessment.id,
        "user_id": current_user,
        "overall_score": result["overall_score"],
        "category": result["category"],
        "domain_scores": result["domain_scores"]
    }


# ============================================================
# 2. COMPLETE AI + RAG ASSESSMENT REPORT
# ============================================================

@router.post("/report")
def assessment_report(
    request: AssessmentRequest,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Validate answers
    # --------------------------------------------------------

    for question_id, answer in request.answers.items():

        if answer < 0 or answer > 4:

            return {
                "error": (
                    f"Invalid answer for question "
                    f"{question_id}. "
                    "Answer must be between 0 and 4."
                )
            }

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    safety_result = check_safety(request.answers)

    if safety_result["safety_concern"]:

        return {
            "safety_override": True,
            "overall_score": None,
            "category": "safety_concern",
            "safety": safety_result,
            "recommendation": (
                "Please seek immediate support from a "
                "qualified mental-health professional or "
                "appropriate local emergency/crisis services."
            )
        }

    # --------------------------------------------------------
    # Calculate assessment
    # --------------------------------------------------------

    result = calculate_assessment(
        request.answers
    )

    # --------------------------------------------------------
    # Save assessment
    # --------------------------------------------------------

    assessment = Assessment(
        user_id=current_user,
        overall_score=result["overall_score"],
        category=result["category"],
        domain_scores=result["domain_scores"],
        answers=request.answers
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # --------------------------------------------------------
    # Generate AI + RAG report
    # --------------------------------------------------------

    report = generate_assessment_report(
        overall_score=result["overall_score"],
        category=result["category"],
        domain_scores=result["domain_scores"]
    )

    # --------------------------------------------------------
    # Return complete report
    # --------------------------------------------------------

    return {
        "assessment_id": assessment.id,
        "user_id": current_user,
        "overall_score": result["overall_score"],
        "category": result["category"],
        "domain_scores": result["domain_scores"],
        "report": report
    }


# ============================================================
# 3. REASSESSMENT
# ============================================================

@router.post("/reassess")
def reassess(
    request: ReassessmentRequest,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Validate answers
    # --------------------------------------------------------

    for question_id, answer in request.answers.items():

        if answer < 0 or answer > 4:

            return {
                "error": (
                    f"Invalid answer for question "
                    f"{question_id}. "
                    "Answer must be between 0 and 4."
                )
            }

    # --------------------------------------------------------
    # Check answers exist
    # --------------------------------------------------------

    count = len(request.answers)

    if count == 0:

        return {
            "error": "No reassessment answers provided."
        }

    # --------------------------------------------------------
    # Find previous assessment belonging to this user
    # --------------------------------------------------------

    previous_assessment = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user
        )
        .order_by(
            Assessment.created_at.desc()
        )
        .first()
    )

    if previous_assessment is None:

        raise HTTPException(
            status_code=404,
            detail="No previous assessment found."
        )

    # --------------------------------------------------------
    # Calculate reassessment score
    # --------------------------------------------------------

    total = sum(request.answers.values())

    average = total / count

    # Convert 0-4 scale to 1-10 scale
    reassessment_score = round(
        1 + (average / 4) * 9,
        2
    )

    # --------------------------------------------------------
    # Determine category
    # --------------------------------------------------------

    if reassessment_score <= 3.5:

        category = "significant_concern"

        recommendation = (
            "The responses suggest that additional professional "
            "support may be beneficial. Consider speaking with "
            "a qualified mental-health professional."
        )

    elif reassessment_score <= 6.5:

        category = "moderate_concern"

        recommendation = (
            "The responses still indicate some level of concern. "
            "Consider speaking with a qualified mental-health "
            "professional for further evaluation."
        )

    else:

        category = "relatively_stable"

        recommendation = (
            "The responses indicate relatively lower levels of "
            "reported difficulty. Continue healthy coping "
            "strategies and self-care."
        )

    # --------------------------------------------------------
    # Compare with previous assessment
    # --------------------------------------------------------

    previous_score = previous_assessment.overall_score

    change = round(
        reassessment_score - previous_score,
        2
    )

    if change < -0.1:

        status = "improved"

        message = (
            "Your assessment score has improved."
        )

    elif change > 0.1:

        status = "worsened"

        message = (
            "Your assessment score has increased. "
            "Consider discussing your results with a "
            "qualified mental-health professional."
        )

    else:

        status = "stable"

        message = (
            "Your assessment score has remained relatively stable."
        )

    # --------------------------------------------------------
    # Domain comparison
    # --------------------------------------------------------

    domain_comparison = {}

    previous_domains = (
        previous_assessment.domain_scores or {}
    )

    domains = [
        "mood",
        "anxiety",
        "stress",
        "sleep",
        "functioning",
        "social",
        "coping"
    ]

    for domain in domains:

        previous_domain_score = previous_domains.get(
            domain,
            previous_score
        )

        current_domain_score = reassessment_score

        domain_change = round(
            current_domain_score - previous_domain_score,
            2
        )

        if domain_change < -0.1:

            domain_status = "improved"

        elif domain_change > 0.1:

            domain_status = "worsened"

        else:

            domain_status = "stable"

        domain_comparison[domain] = {
            "previous": previous_domain_score,
            "current": current_domain_score,
            "change": domain_change,
            "status": domain_status
        }

    # --------------------------------------------------------
    # Save reassessment as a new assessment
    # --------------------------------------------------------

    reassessment_category = {
        "category": category,
        "label": (
            "Significant concern"
            if category == "significant_concern"
            else
            "Moderate concern"
            if category == "moderate_concern"
            else
            "Relatively stable"
        ),
        "action": recommendation
    }

    reassessment_domain_scores = {
        domain: reassessment_score
        for domain in domains
    }

    new_assessment = Assessment(
        user_id=current_user,
        overall_score=reassessment_score,
        category=reassessment_category,
        domain_scores=reassessment_domain_scores,
        answers=request.answers
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    # --------------------------------------------------------
    # Return reassessment
    # --------------------------------------------------------

    return {
        "previous_assessment_id": previous_assessment.id,
        "new_assessment_id": new_assessment.id,
        "reassessment_score": reassessment_score,
        "category": category,
        "recommendation": recommendation,
        "comparison": {
            "previous_score": previous_score,
            "new_score": reassessment_score,
            "change": change,
            "status": status,
            "message": message,
            "domain_comparison": domain_comparison
        }
    }


# ============================================================
# 4. ASSESSMENT HISTORY
# ============================================================

@router.get("/history")
def assessment_history(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user
        )
        .order_by(
            Assessment.created_at.desc()
        )
        .all()
    )

    return {
        "user_id": current_user,
        "count": len(assessments),
        "assessments": [
            {
                "assessment_id": assessment.id,
                "overall_score": assessment.overall_score,
                "category": assessment.category,
                "domain_scores": assessment.domain_scores,
                "created_at": assessment.created_at
            }
            for assessment in assessments
        ]
    }


# ============================================================
# 5. ASSESSMENT DETAILS
# ============================================================

@router.get("/details/{assessment_id}")
def assessment_details(
    assessment_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user
        )
        .first()
    )

    if assessment is None:

        raise HTTPException(
            status_code=404,
            detail="Assessment not found."
        )

    return {
        "assessment_id": assessment.id,
        "user_id": assessment.user_id,
        "overall_score": assessment.overall_score,
        "category": assessment.category,
        "domain_scores": assessment.domain_scores,
        "answers": assessment.answers,
        "created_at": assessment.created_at
    }


# ============================================================
# 6. ASSESSMENT PROGRESS
# ============================================================

@router.get("/progress")
def assessment_progress(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user
        )
        .order_by(
            Assessment.created_at.asc()
        )
        .all()
    )

    return {
        "user_id": current_user,
        "count": len(assessments),
        "progress": [
            {
                "assessment_id": assessment.id,
                "overall_score": assessment.overall_score,
                "category": assessment.category,
                "domain_scores": assessment.domain_scores,
                "created_at": assessment.created_at
            }
            for assessment in assessments
        ]
    }