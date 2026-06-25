from time import perf_counter

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

    answer = (
        f"This is a mock ESG answer for {request.company}. "
        f"Later, this endpoint will retrieve relevant ESG report chunks "
        f"and generate a cited response to: {request.question}"
    )

    latency_ms = int((perf_counter() - start_time) * 1000)

    return QueryResponse(
        answer=answer,
        citations=[],
        company=request.company,
        pillar=request.pillar,
        latency_ms=latency_ms,
    )