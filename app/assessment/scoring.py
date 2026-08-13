from .questions import QUESTIONS
from .domains import DOMAINS
from app.services.rag import retrieve_domain_evidence


def calculate_domain_scores(answers: dict[int, int]):
    """
    Calculate the average score for each assessment domain.

    Each answer should be between 0 and 4.
    """

    domain_totals = {}
    domain_counts = {}

    for question in QUESTIONS:
        question_id = question["id"]
        domain = question["domain"]

        # Safety questions are handled separately by safety.py
        if domain == "safety":
            continue

        if question_id not in answers:
            continue

        score = answers[question_id]

        domain_totals[domain] = (
            domain_totals.get(domain, 0) + score
        )

        domain_counts[domain] = (
            domain_counts.get(domain, 0) + 1
        )

    domain_scores = {}

    for domain, total in domain_totals.items():

        count = domain_counts[domain]

        average = total / count

        # Convert 0-4 into 1-10
        rating = 1 + (average / 4) * 9

        domain_scores[domain] = round(rating, 2)

    return domain_scores


def calculate_overall_score(domain_scores: dict):
    """
    Calculate the overall 1-10 assessment rating.
    """

    if not domain_scores:
        return 1.0

    average = sum(domain_scores.values()) / len(domain_scores)

    return round(average, 2)


def get_rating_category(score: float):
    """
    Convert the numerical score into a support category.
    """

    if score <= 3.5:
        return {
            "category": "significant_concern",
            "label": "Significant concern",
            "action": (
                "Consider speaking with a qualified "
                "mental-health professional."
            )
        }

    elif score <= 6.5:
        return {
            "category": "moderate_concern",
            "label": "Moderate concern",
            "action": (
                "Continue with additional assessment "
                "questions and reassess."
            )
        }

    else:
        return {
            "category": "relatively_stable",
            "label": "Relatively stable",
            "action": (
                "Continue healthy coping strategies "
                "and self-care."
            )
        }


def calculate_assessment(answers: dict[int, int]):
    """
    Calculate assessment result and retrieve
    evidence relevant to the highest-scoring domains.
    """

    domain_scores = calculate_domain_scores(answers)

    overall_score = calculate_overall_score(
        domain_scores
    )

    category = get_rating_category(
        overall_score
    )

    # Retrieve evidence relevant to the assessment
    evidence = retrieve_domain_evidence(
        domain_scores
    )

    return {
        "overall_score": overall_score,
        "category": category,
        "domain_scores": domain_scores,
        "evidence": evidence
    }

if __name__ == "__main__":

    # Example answers
    test_answers = {
        question["id"]: 2
        for question in QUESTIONS
    }

    result = calculate_assessment(
        test_answers
    )

    print("\n==============================")
    print("ASSESSMENT RESULT")
    print("==============================")

    print(
        f"\nOverall score: "
        f"{result['overall_score']}/10"
    )

    print(
        f"Category: "
        f"{result['category']['label']}"
    )

    print(
        f"Action: "
        f"{result['category']['action']}"
    )

    print("\nDomain scores:")

    for domain, score in result["domain_scores"].items():

        domain_name = DOMAINS[domain]["name"]

        print(
            f"  {domain_name}: "
            f"{score}/10"
        )
def compare_assessments(
    previous_score: float,
    new_score: float,
    previous_domains: dict,
    new_domains: dict
):
    """
    Compare the previous assessment with the new reassessment.
    Lower scores indicate less concern.
    """

    change = round(new_score - previous_score, 2)

    if change < -0.5:
        status = "improved"
        message = "Your assessment score has improved."
    elif change > 0.5:
        status = "worsened"
        message = "Your assessment score has increased and may need further attention."
    else:
        status = "unchanged"
        message = "Your assessment score has remained relatively stable."

    domain_comparison = {}

    for domain in new_domains:

        previous = previous_domains.get(domain)
        current = new_domains[domain]

        if previous is None:
            continue

        domain_change = round(current - previous, 2)

        if domain_change < -0.5:
            domain_status = "improved"
        elif domain_change > 0.5:
            domain_status = "worsened"
        else:
            domain_status = "unchanged"

        domain_comparison[domain] = {
            "previous": previous,
            "current": current,
            "change": domain_change,
            "status": domain_status
        }

    return {
        "previous_score": previous_score,
        "new_score": new_score,
        "change": change,
        "status": status,
        "message": message,
        "domain_comparison": domain_comparison
    }