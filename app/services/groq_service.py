import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set in the .env file."
    )


client = Groq(
    api_key=GROQ_API_KEY
)


def generate_assessment_interpretation(prompt: str) -> str:
    """
    Send the assessment prompt to Groq and return
    the generated interpretation.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the AI interpretation component "
                    "of MindBridge. Provide supportive, cautious "
                    "and evidence-grounded mental-health information. "
                    "Never diagnose the user."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    return response.choices[0].message.content