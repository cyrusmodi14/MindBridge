from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)


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