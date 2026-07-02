from models.embeddings import embed_text
from rag.vector_store import get_documents_collection


def retrieve_document_chunks(
    query: str,
    company_name: str | None = None,
    pillar: str | None = None,
    year: int | None = None,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve the most relevant ESG document chunks for a query.
    """
    collection = get_documents_collection()
    query_embedding = embed_text(query)

    where_filter = {}

    if company_name:
        where_filter["company_name"] = company_name

    if pillar:
        where_filter["esg_pillar"] = pillar

    if year:
        where_filter["document_year"] = year

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter if where_filter else None,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(documents, metadatas, distances, strict=True):
        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks