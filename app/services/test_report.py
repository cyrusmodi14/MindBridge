from app.services.assessment_report import (
    generate_assessment_report
)


domain_scores = {
    "mood": 5.5,
    "anxiety": 5.5,
    "stress": 5.5,
    "sleep": 5.5,
    "functioning": 5.5,
    "social": 5.5,
    "coping": 5.5
}


category = {
    "category": "moderate_concern",
    "label": "Moderate concern",
    "action": (
        "Continue with additional assessment "
        "questions and reassess."
    )
}


report = generate_assessment_report(
    overall_score=5.5,
    category=category,
    domain_scores=domain_scores
)


print("\n==============================")
print("Solace ASSESSMENT REPORT")
print("==============================")

print("\nOVERALL SCORE:")
print(report["overall_score"])

print("\nCATEGORY:")
print(report["category"])

print("\nDOMAIN SCORES:")
print(report["domain_scores"])

print("\nAI INTERPRETATION:")
print(report["interpretation"])

print("\nEVIDENCE SOURCES:")

for domain, data in report["evidence"].items():

    print(f"\n--- {domain.upper()} ---")

    for result in data["results"]:

        metadata = result.get(
            "metadata",
            {}
        )

        print(
            metadata.get(
                "source",
                "Unknown"
            ),
            "|",
            metadata.get(
                "document",
                "Unknown"
            )
        )