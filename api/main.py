from time import perf_counter
from rag.retriever import retrieve_document_chunks
from fastapi import FastAPI, HTTPException
from models.llm import generate_answer
from api.schemas import QueryRequest, QueryResponse
from data.company_metadata import load_companies, load_company_by_ticker

app = FastAPI(
    title="ESG Sentinel API",
    description="Backend API for ESG intelligence and sentiment analysis.",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "service": "ESG Sentinel API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "query": "/query",
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ESG Sentinel API"}

@app.get("/companies")
def get_companies():
    try:
        companies = load_companies()
    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {"companies": companies}

@app.post("/query", response_model=QueryResponse)
def query_esg(request: QueryRequest):
    start_time = perf_counter()

    company_name = request.company

    try:
        company_metadata = load_company_by_ticker(request.company)
        company_name = company_metadata["company_name"]
    except ValueError:
        pass

    retrieved_chunks = retrieve_document_chunks(
        query=request.question,
        company_name=company_name,
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
        try:
            answer = generate_answer(request.question, retrieved_chunks)
        except ValueError as error:
            raise HTTPException(status_code=500, detail=str(error)) from error
        except Exception as error:
            raise HTTPException(
                status_code=502,
                detail="LLM answer generation failed. Please try again later.",
            ) from error
    else:
        answer = f"No relevant ESG evidence found for {request.company}."

    latency_ms = int((perf_counter() - start_time) * 1000)

    return QueryResponse(
        answer=answer,
        citations=citations,
        company=company_name,
        pillar=request.pillar,
        latency_ms=latency_ms,
    )

@app.post("/retrieve")
def retrieve_esg(request: QueryRequest):
    company_name = request.company

    try:
        company_metadata = load_company_by_ticker(request.company)
        company_name = company_metadata["company_name"]
    except ValueError:
        pass

    retrieved_chunks = retrieve_document_chunks(
        query=request.question,
        company_name=company_name,
        pillar=request.pillar,
        year=request.year,
        top_k=3,
    )

    return {
        "company": company_name,
        "results": retrieved_chunks,
    }