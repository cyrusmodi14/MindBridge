from collections import defaultdict

from app.services.retrieve import retrieve


EVIDENCE_LEVEL_WEIGHTS = {
    "high": 1.00,
    "medium": 0.75,
    "low": 0.50,
    "unknown": 0.40,
}


AUTHORITY_WEIGHTS = {
    "official": 1.00,
    "academic": 0.95,
    "clinical": 0.95,
    "professional": 0.90,
    "unknown": 0.50,
}


CATEGORY_WEIGHTS = {
    "guideline": 1.00,
    "assessment": 0.95,
    "research": 0.90,
    "case_report": 0.70,
    "therapist_resource": 0.65,
    "self_help": 0.60,
    "unknown": 0.40,
}


def calculate_evidence_score(result):

    metadata = result["metadata"]

    similarity = result["similarity_score"]

    evidence_level = metadata.get(
        "evidence_level",
        "unknown"
    )

    authority = metadata.get(
        "authority",
        "unknown"
    )

    category = metadata.get(
        "category",
        "unknown"
    )

    evidence_weight = EVIDENCE_LEVEL_WEIGHTS.get(
        evidence_level,
        0.40
    )

    authority_weight = AUTHORITY_WEIGHTS.get(
        authority,
        0.50
    )

    category_weight = CATEGORY_WEIGHTS.get(
        category,
        0.40
    )

    score = (
        similarity
        * evidence_weight
        * authority_weight
        * category_weight
    )

    return score


def rank_evidence(
    query: str,
    candidate_count: int = 12,
    final_count: int = 5,
    max_chunks_per_document: int = 2
):

    candidates = retrieve(
        query=query,
        n_results=candidate_count
    )

    ranked = []

    for result in candidates:

        score = calculate_evidence_score(
            result
        )

        result["evidence_score"] = score

        ranked.append(result)

    ranked.sort(
        key=lambda x: x["evidence_score"],
        reverse=True
    )

    selected = []

    document_counts = defaultdict(int)

    for result in ranked:

        document = result["metadata"].get(
            "document",
            "unknown"
        )

        if (
            document_counts[document]
            >= max_chunks_per_document
        ):
            continue

        selected.append(result)

        document_counts[document] += 1

        if len(selected) >= final_count:
            break

    return selected


if __name__ == "__main__":

    query = (
        "I am experiencing a lot of "
        "stress and difficulty coping "
        "with everyday problems."
    )

    results = rank_evidence(
        query=query,
        candidate_count=12,
        final_count=5
    )

    print("\n")
    print("=" * 70)
    print("RANKED EVIDENCE")
    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1
    ):

        metadata = result["metadata"]

        print("\n" + "-" * 70)

        print(
            f"RESULT {index}"
        )

        print("-" * 70)

        print(
            "Evidence score:",
            round(
                result["evidence_score"],
                4
            )
        )

        print(
            "Similarity:",
            round(
                result["similarity_score"],
                4
            )
        )

        print(
            "Source:",
            metadata.get(
                "source",
                "unknown"
            )
        )

        print(
            "Document:",
            metadata.get(
                "document",
                "unknown"
            )
        )

        print(
            "Category:",
            metadata.get(
                "category",
                "unknown"
            )
        )

        print(
            "Evidence level:",
            metadata.get(
                "evidence_level",
                "unknown"
            )
        )

        print(
            "Authority:",
            metadata.get(
                "authority",
                "unknown"
            )
        )

        print(
            "Page:",
            metadata.get(
                "page",
                "unknown"
            )
        )

        print(
            "\nText:"
        )

        print(
            result["text"][:700]
        )