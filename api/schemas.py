from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    company: str
    question: str
    pillar: Optional[str] = None
    year: Optional[int] = None


class Citation(BaseModel):
    source: str
    page: Optional[int] = None
    date: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    company: str
    pillar: Optional[str] = None
    latency_ms: int