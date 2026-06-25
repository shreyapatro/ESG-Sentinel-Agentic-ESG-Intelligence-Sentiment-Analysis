from pathlib import Path

import chromadb


CHROMA_PERSIST_DIR = Path("rag/vector_store")


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Create a persistent ChromaDB client.
    Data will be saved inside rag/vector_store.
    """
    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))


def get_documents_collection():
    """
    Get or create the ESG documents collection.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name="esg_documents")


def store_document_chunks(chunks: list[dict], embeddings: list[list[float]]) -> None:
    """
    Store document chunks and their embeddings in ChromaDB.
    """
    collection = get_documents_collection()

    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "company_name": chunk["company_name"],
            "ticker": chunk["ticker"],
            "document_year": chunk["document_year"],
            "document_type": chunk["document_type"],
            "esg_pillar": chunk["esg_pillar"],
            "source_document": chunk["source_document"],
            "page_number": chunk["page_number"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )