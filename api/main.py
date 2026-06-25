from time import perf_counter
from rag.retriever import retrieve_document_chunks
from fastapi import FastAPI

from api.schemas import QueryRequest, QueryResponse

app = FastAPI(
    title="ESG Sentinel API",
    description="Backend API for ESG intelligence and sentiment analysis.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ESG Sentinel API"}


@app.post("/query", response_model=QueryResponse)
def query_esg(request: QueryRequest):
    start_time = perf_counter()

    retrieved_chunks = retrieve_document_chunks(
        query=request.question,
        company_name=request.company,
        pillar=request.pillar,
        year=request.year,
        top_k=3,
    )

    citations = [
        {
            "source": chunk["metadata"]["source_document"],
            "page": chunk["metadata"]["page_number"],
            "text": chunk["text"][:300],
        }
        for chunk in retrieved_chunks
    ]

    if retrieved_chunks:
        answer = (
            f"Found {len(retrieved_chunks)} relevant ESG evidence chunks for "
            f"{request.company}. LLM synthesis will be added in the next stage."
        )
    else:
        answer = f"No relevant ESG evidence found for {request.company}."

    latency_ms = int((perf_counter() - start_time) * 1000)

    return QueryResponse(
        answer=answer,
        citations=citations,
        company=request.company,
        pillar=request.pillar,
        latency_ms=latency_ms,
    )