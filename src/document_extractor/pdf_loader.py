
from pathlib import Path

import pymupdf


def extract_pdf_pages(pdf_path: str) -> list[dict]:
    """Extract text from a PDF, preserving source and page metadata."""

    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Input must be a PDF file.")

    pages = []

    with pymupdf.open(path) as document:
        if document.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported yet.")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text(sort=True).strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text,
                    "source": path.name,
                })

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be scanned."
        )

    return pages


if __name__ == "__main__":
    pdf_path = input("Enter PDF path: ").strip()
    pages = extract_pdf_pages(pdf_path)

    print(f"Extracted {len(pages)} pages with text.")

    for item in pages[:2]:
        print(f"\n--- Page {item['page']} ---")
        print(item["text"][:1000])
