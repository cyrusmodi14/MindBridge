import json
from pathlib import Path

from app.services.document_processor import extract_pdf_pages
from app.services.chunker import chunk_text
from app.services.vector_store import collection


KNOWLEDGE_BASE = Path("knowledge_base")

METADATA_FILE = KNOWLEDGE_BASE / "metadata.json"


CATEGORY_MAP = {
    "guidelines": "guideline",
    "assessments": "assessment",
    "research": "research",
    "case_reports": "case_report",
    "therapist_resources": "therapist_resource",
    "self_help": "self_help",
}


def load_metadata():
    """
    Load document metadata from metadata.json.
    """

    if not METADATA_FILE.exists():
        print(
            "metadata.json not found. "
            "Using default metadata."
        )

        return {}

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def ingest_pdf(
    pdf_path: Path,
    category: str,
    metadata: dict
):

    print(
        f"\nProcessing: {pdf_path.name}"
    )

    pages = extract_pdf_pages(
        str(pdf_path)
    )

    documents = []
    metadatas = []
    ids = []

    chunk_counter = 0

    source = metadata.get(
        "source",
        "unknown"
    )

    evidence_level = metadata.get(
        "evidence_level",
        "unknown"
    )

    authority = metadata.get(
        "authority",
        "unknown"
    )

    document_id = pdf_path.stem

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for chunk in chunks:

            chunk_id = (
                f"{document_id}"
                f"_p{page['page']}"
                f"_c{chunk_counter}"
            )

            documents.append(chunk)

            metadatas.append({
                "document_id": document_id,
                "document": pdf_path.name,
                "source": source,
                "category": category,
                "evidence_level": evidence_level,
                "authority": authority,
                "page": page["page"]
            })

            ids.append(chunk_id)

            chunk_counter += 1

    if not documents:

        print(
            f"No text found in "
            f"{pdf_path.name}"
        )

        return 0

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(
        f"Ingested {len(documents)} chunks."
    )

    print(
        f"Source: {source}"
    )

    print(
        f"Category: {category}"
    )

    print(
        f"Evidence level: {evidence_level}"
    )

    print(
        f"Authority: {authority}"
    )

    return len(documents)


def ingest_knowledge_base():

    metadata = load_metadata()

    pdf_files = list(
        KNOWLEDGE_BASE.rglob("*.pdf")
    )

    if not pdf_files:

        print(
            "No PDF files found "
            "in knowledge_base/"
        )

        return

    print(
        f"Found {len(pdf_files)} PDF(s)."
    )

    total_chunks = 0

    for pdf_path in pdf_files:

        folder_name = (
            pdf_path.parent.name
        )

        category = CATEGORY_MAP.get(
            folder_name,
            "unknown"
        )

        document_metadata = metadata.get(
            pdf_path.name,
            {}
        )

        total_chunks += ingest_pdf(
            pdf_path=pdf_path,
            category=category,
            metadata=document_metadata
        )

    print(
        "\n================================"
    )

    print(
        f"Total chunks ingested: "
        f"{total_chunks}"
    )

    print(
        "================================"
    )


if __name__ == "__main__":

    ingest_knowledge_base()