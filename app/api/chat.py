from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.database.models import User

from app.services.groq_service import generate_chat_response
from app.services.rag import retrieve_knowledge


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
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    if len(message) > 4000:
        raise HTTPException(
            status_code=400,
            detail="Message is too long."
        )

    try:
        knowledge = retrieve_knowledge(
            message,
            n_results=4
        )

        context_parts = []

        for item in knowledge:
            text = item.get("text")

            if text:
                context_parts.append(text)

        context = "\n\n".join(
            context_parts
        )

        response = generate_chat_response(
            message=message,
            context=context
        )

        return {
            "response": response
        }

    except Exception as exc:

        print(
            f"Chat generation error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response right now."
        )