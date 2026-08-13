from pathlib import Path

import pymupdf


def extract_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract readable text from a PDF page-by-page.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = []

    with pymupdf.open(pdf_path) as document:

        for page_number, page in enumerate(
            document,
            start=1
        ):

            # Extract blocks instead of raw page text.
            blocks = page.get_text(
                "blocks"
            )

            page_parts = []

            for block in blocks:

                # Block structure:
                # x0, y0, x1, y1, text, ...

                text = block[4].strip()

                if not text:
                    continue

                # Ignore extremely short fragments.
                if len(text) < 20:
                    continue

                page_parts.append(text)

            page_text = "\n\n".join(
                page_parts
            )

            if page_text.strip():

                pages.append({
                    "text": page_text,
                    "page": page_number
                })

    return pages