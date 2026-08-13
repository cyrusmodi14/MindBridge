from app.services.vector_store import collection


EVIDENCE_WEIGHTS = {
    "guideline": 1.00,
    "assessment": 0.95,
    "research": 0.90,
    "case_report": 0.70,
    "therapist_resource": 0.65,
    "self_help": 0.60,
}


def retrieve(
    query: str,
    n_results: int = 5
):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        category = metadata.get(
            "category",
            "unknown"
        )

        evidence_weight = EVIDENCE_WEIGHTS.get(
            category,
            0.50
        )

        similarity_score = 1 / (
            1 + distance
        )

        final_score = (
            similarity_score
            * evidence_weight
        )

        retrieved.append({
            "text": document,
            "metadata": metadata,
            "distance": distance,
            "similarity_score": similarity_score,
            "evidence_weight": evidence_weight,
            "final_score": final_score
        })

    retrieved.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return retrieved


if __name__ == "__main__":

    query = (
        "How can someone cope "
        "with overwhelming stress?"
    )

    results = retrieve(query)

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "=" * 70)

        print(
            f"RESULT {index}"
        )

        print("=" * 70)

        print(
            "\nFinal score:",
            round(
                result["final_score"],
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
            "Evidence weight:",
            result["evidence_weight"]
        )

        print(
            "\nMetadata:"
        )

        print(
            result["metadata"]
        )

        print(
            "\nText:"
        )

        print(
            result["text"][:1000]
        )