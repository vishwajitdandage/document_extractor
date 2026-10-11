
from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """Generate text embeddings using a local model."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return vectors.tolist()

    def embed_query(self, question: str) -> list[float]:
        vector = self.model.encode(
            [question],
            normalize_embeddings=True,
        )
        return vector[0].tolist()
