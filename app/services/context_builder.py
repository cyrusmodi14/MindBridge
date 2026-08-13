from app.services.evidence_ranker import rank_evidence


def build_context(
    query: str,
    n_results: int = 5
):
    """
    Retrieve relevant evidence and convert it
    into structured context for the LLM.
    """

    results = rank_evidence(
    query=query,
    candidate_count=12,
    final_count=n_results
)

    if not results:
        return {
            "context": "",
            "sources": []
        }

    context_parts = []
    sources = []

    for index, result in enumerate(
        results,
        start=1
    ):

        metadata = result["metadata"]

        source = metadata.get(
            "source",
            "Unknown"
        )

        document = metadata.get(
            "document",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        category = metadata.get(
            "category",
            "Unknown"
        )

        evidence_level = metadata.get(
            "evidence_level",
            "Unknown"
        )

        authority = metadata.get(
            "authority",
            "Unknown"
        )

        text = result["text"]

        context_parts.append(
            f"""
SOURCE {index}

Source: {source}
Document: {document}
Page: {page}
Category: {category}
Evidence level: {evidence_level}
Authority: {authority}

Relevant information:
{text}
"""
        )

        sources.append({
            "source": source,
            "document": document,
            "page": page,
            "category": category,
            "evidence_level": evidence_level,
            "authority": authority
        })

    context = "\n".join(
        context_parts
    )

    return {
        "context": context,
        "sources": sources
    }


if __name__ == "__main__":

    query = (
        "I am experiencing a lot of "
        "stress and difficulty coping "
        "with everyday problems."
    )

    result = build_context(
        query=query,
        n_results=5
    )

    print("\n")
    print("=" * 70)
    print("GENERATED CONTEXT")
    print("=" * 70)

    print(
        result["context"]
    )

    print("\n")
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for source in result["sources"]:

        print(source)