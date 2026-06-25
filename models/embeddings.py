from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_text(text: str) -> list[float]:
    """
    Convert one text string into an embedding vector.
    """
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple text strings into embedding vectors.
    """
    model = get_embedding_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()