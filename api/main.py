from fastapi import FastAPI

app = FastAPI(
    title="ESG Sentinel API",
    description="Backend API for ESG intelligence and sentiment analysis.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ESG Sentinel API"}