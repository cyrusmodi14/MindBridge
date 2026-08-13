from app.services.retrieve import retrieve
from app.services.ai_interpreter import build_assessment_prompt
from app.services.groq_service import generate_assessment_interpretation


def retrieve_assessment_evidence(domain_scores: dict):
    """
    Retrieve relevant psychological evidence for each
    assessment domain.
    """

    evidence = {}

    for domain, score in domain_scores.items():

        query = (
            f"psychological information about {domain} "
            f"and difficulties related to {domain}"
        )

        results = retrieve(
            query=query,
            n_results=3
        )

        evidence[domain] = {
            "score": score,
            "results": results
        }

    return evidence


def generate_assessment_report(
    overall_score: float,
    category: dict,
    domain_scores: dict
):
    """
    Complete assessment pipeline:

    scores
       ↓
    RAG retrieval
       ↓
    prompt construction
       ↓
    Groq interpretation
    """

    # --------------------------------
    # 1. Retrieve psychology evidence
    # --------------------------------

    evidence = retrieve_assessment_evidence(
        domain_scores
    )

    # --------------------------------
    # 2. Build AI prompt
    # --------------------------------

    prompt = build_assessment_prompt(
        overall_score=overall_score,
        category=category,
        domain_scores=domain_scores,
        evidence=evidence
    )

    # --------------------------------
    # 3. Generate interpretation
    # --------------------------------

    interpretation = generate_assessment_interpretation(
        prompt
    )

    # --------------------------------
    # 4. Return complete report
    # --------------------------------

    return {
        "overall_score": overall_score,
        "category": category,
        "domain_scores": domain_scores,
        "evidence": evidence,
        "interpretation": interpretation
    }