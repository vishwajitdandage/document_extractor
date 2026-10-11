
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 700,
    overlap: int = 100,
) -> list[dict]:
    """Split extracted PDF pages into overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size.")

    chunks = []

    for page in pages:
        text = page["text"].strip()
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Prefer a nearby word boundary.
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start:
                    end = boundary

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "id": (
                        f"{page['source']}-"
                        f"p{page['page']}-c{chunk_index}"
                    ),
                    "text": chunk_text,
                    "source": page["source"],
                    "page": page["page"],
                    "chunk_index": chunk_index,
                })
                chunk_index += 1

            if end >= len(text):
                break

            start = max(start + 1, end - overlap)

    return chunks
