
import chromadb


class VectorStore:
    """Persistent ChromaDB storage for document chunks."""

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)

        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Each chunk must have exactly one embedding."
            )

        if not chunks:
            return

        self.collection.upsert(
            ids=[chunk["id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "chunk_index": chunk["chunk_index"],
                }
                for chunk in chunks
            ],
        )

    def delete_source(self, source: str) -> None:
        """Delete all indexed chunks belonging to one source document."""
        self.collection.delete(where={"source": source})

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
