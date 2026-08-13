from app.services.ai_interpreter import build_assessment_prompt


test_domain_scores = {
    "mood": 5.5,
    "anxiety": 5.5,
    "stress": 5.5,
    "sleep": 5.5,
    "functioning": 5.5,
    "social": 5.5,
    "coping": 5.5,
}


test_category = {
    "category": "moderate_concern",
    "label": "Moderate concern",
    "action": "Continue with additional assessment questions and reassess."
}


test_evidence = {
    "mood": {
        "score": 5.5,
        "results": [
            {
                "text": (
                    "In stressful situations, difficult thoughts and "
                    "feelings can affect how people respond."
                ),
                "metadata": {
                    "source": "WHO",
                    "document": "doing_what_matters.pdf",
                    "category": "self_help",
                    "evidence_level": "high",
                    "authority": "official",
                },
            }
        ],
    }
}


prompt = build_assessment_prompt(
    overall_score=5.5,
    category=test_category,
    domain_scores=test_domain_scores,
    evidence=test_evidence,
)


print("\n==============================")
print("GENERATED AI PROMPT")
print("==============================\n")

print(prompt)