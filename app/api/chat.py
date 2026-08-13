from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.database.models import User

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    # Connect this to your existing
    # Groq/RAG service.

    response = "AI response goes here."

    return {
        "response": response
    }