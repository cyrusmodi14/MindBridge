import re


def clean_text(text: str) -> str:
    """
    Clean common PDF extraction artifacts.
    """

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 75
) -> list[str]:

    text = clean_text(text)

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        ).strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks