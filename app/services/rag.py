from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)


# ==============================
# ChromaDB configuration
# ==============================

VECTOR_DB_PATH = Path("vector_db")
COLLECTION_NAME = "Solace_knowledge"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


# ==============================
# General retrieval
# ==============================

def retrieve_knowledge(query: str, n_results: int = 5):
    """
    Retrieve relevant psychology knowledge from ChromaDB.
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    retrieved = []

    for document, metadata in zip(documents, metadatas):
        retrieved.append({
            "text": document,
            "metadata": metadata
        })

    return retrieved


# ==============================
# Domain-specific retrieval
# ==============================

DOMAIN_QUERIES = {

    "mood": (
        "mood emotional wellbeing sadness low mood "
        "emotional difficulties coping with difficult emotions"
    ),

    "anxiety": (
        "anxiety excessive worry anxious thoughts "
        "fear coping with anxiety emotional regulation"
    ),

    "stress": (
        "stress management psychological stress "
        "coping with stressful situations adversity"
    ),

    "sleep": (
        "sleep problems sleep difficulties rest "
        "relationship between sleep and emotional wellbeing"
    ),

    "functioning": (
        "daily functioning mental wellbeing "
        "difficulty performing everyday activities "
        "work school responsibilities"
    ),

    "social": (
        "social relationships loneliness isolation "
        "social support relationships and mental wellbeing"
    ),

    "coping": (
        "coping strategies psychological coping "
        "healthy ways to manage difficult thoughts "
        "feelings and stressful situations"
    )
}


def retrieve_domain_evidence(
    domain_scores: dict,
    n_results_per_domain: int = 2
):
    """
    Retrieve psychology evidence relevant to the
    user's highest-scoring assessment domains.

    This does NOT diagnose the user.
    It only retrieves relevant evidence for interpretation.
    """

    evidence = {}

    # Sort domains from highest score to lowest score
    sorted_domains = sorted(
        domain_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # Focus on the most concerning domains
    top_domains = sorted_domains[:3]

    for domain, score in top_domains:

        query = DOMAIN_QUERIES.get(domain)

        if not query:
            continue

        results = retrieve_knowledge(
            query,
            n_results=n_results_per_domain
        )

        evidence[domain] = {
            "score": score,
            "results": results
        }

    return evidence