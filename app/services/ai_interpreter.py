from typing import Dict, Any


def build_assessment_prompt(
    overall_score: float,
    category: Dict[str, Any],
    domain_scores: Dict[str, float],
    evidence: Dict[str, Any],
) -> str:
    """
    Build the prompt used by the AI to interpret an assessment.

    The AI must interpret the assessment without diagnosing the user.
    """

    evidence_text = ""

    for domain, data in evidence.items():

        evidence_text += f"\nDOMAIN: {domain}\n"
        evidence_text += f"DOMAIN SCORE: {data.get('score')}\n"

        for result in data.get("results", []):

            text = result.get("text", "")
            metadata = result.get("metadata", {})

            evidence_text += "\nEvidence:\n"
            evidence_text += text[:3000]

            evidence_text += "\nMetadata:\n"
            evidence_text += str(metadata)

            evidence_text += "\n"

    prompt = f"""
You are the assessment interpretation component of MindBridge.

MindBridge is a mental-health support application.

IMPORTANT:
- Do NOT diagnose the user.
- Do NOT claim that a score proves a mental-health disorder.
- Do NOT present the assessment as a clinical diagnosis.
- Explain that the assessment is a screening/support tool.
- Base psychological claims on the supplied evidence.
- Do not invent evidence or citations.
- Use simple, supportive language.
- Do not be alarmist.
- If safety concerns are present, safety instructions take priority.

ASSESSMENT:

Overall score:
{overall_score}/10

Category:
{category.get("label")}

Category action:
{category.get("action")}

Domain scores:
{domain_scores}

RETRIEVED PSYCHOLOGY EVIDENCE:
{evidence_text}

Generate a concise assessment interpretation.

Return the following sections:

1. SUMMARY
Give a short explanation of what the overall result means.

2. AREAS TO PAY ATTENTION TO
Identify the domains with the most notable scores.

3. WHAT THE EVIDENCE SUGGESTS
Explain the relevant psychological information from the retrieved evidence.

4. RECOMMENDED NEXT STEPS
Give practical, low-risk suggestions appropriate for a mental-health
support application.

5. DISCLAIMER
Clearly state that this is not a diagnosis and does not replace
assessment by a qualified mental-health professional.

Do not mention information that is not supported by the assessment
or retrieved evidence.
"""

    return prompt