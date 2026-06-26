from hashlib import md5
from pathlib import Path

import fitz


def extract_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF while preserving page numbers.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with fitz.open(path) as document:
        for page_index, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(
                    {
                        "page_number": page_index,
                        "text": text,
                        "source_document": path.name,
                    }
                )

    return pages


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping character chunks.

    This is a simple first version. Later, we can upgrade this to token-based chunking.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def make_chunk_id(
    source_document: str,
    page_number: int,
    chunk_index: int,
    text: str,
) -> str:
    """
    Create a stable chunk ID so repeated ingestion does not create duplicates.
    """
    raw_id = f"{source_document}:{page_number}:{chunk_index}:{text}"
    return md5(raw_id.encode("utf-8")).hexdigest()


def build_document_chunks(
    pages: list[dict],
    company_name: str,
    ticker: str,
    document_year: int,
    document_type: str,
    esg_pillar: str = "General",
) -> list[dict]:
    """
    Convert extracted PDF pages into metadata-rich chunks.
    """
    document_chunks = []

    for page in pages:
        text_chunks = chunk_text(page["text"])

        for chunk_index, text in enumerate(text_chunks):
            document_chunks.append(
                {
                    "chunk_id": make_chunk_id(
                        source_document=page["source_document"],
                        page_number=page["page_number"],
                        chunk_index=chunk_index,
                        text=text,
                    ),
                    "company_name": company_name,
                    "ticker": ticker,
                    "document_year": document_year,
                    "document_type": document_type,
                    "esg_pillar": esg_pillar,
                    "source_document": page["source_document"],
                    "page_number": page["page_number"],
                    "text": text,
                }
            )

    return document_chunks