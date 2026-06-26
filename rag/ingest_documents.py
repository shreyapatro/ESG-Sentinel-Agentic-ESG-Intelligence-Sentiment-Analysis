import argparse
from pathlib import Path

from agents.document_ingestor import build_document_chunks, extract_pdf_pages
from models.embeddings import embed_texts
from rag.vector_store import store_document_chunks


def ingest_pdf(
    pdf_path: str,
    company_name: str,
    ticker: str,
    document_year: int,
    document_type: str,
    esg_pillar: str,
) -> None:
    pages = extract_pdf_pages(pdf_path)

    chunks = build_document_chunks(
        pages=pages,
        company_name=company_name,
        ticker=ticker,
        document_year=document_year,
        document_type=document_type,
        esg_pillar=esg_pillar,
    )

    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(chunk_texts)

    print("Storing chunks in ChromaDB...")
    store_document_chunks(chunks, embeddings)
    print("Stored chunks in ChromaDB collection: esg_documents")

    print(f"Extracted {len(pages)} pages from {pdf_path}")
    print(f"Created {len(chunks)} chunks")
    print(f"Created {len(embeddings)} embeddings")

    if embeddings:
        print(f"Each embedding has {len(embeddings[0])} dimensions")

    for chunk, embedding in zip(chunks[:3], embeddings[:3]):
        preview = chunk["text"][:200].replace("\n", " ")
        print(f"\nChunk {chunk['chunk_id']}")
        print(f"Company: {chunk['company_name']} | Page: {chunk['page_number']}")
        print(f"Embedding preview: {embedding[:5]}")
        print(preview)


def main():
    parser = argparse.ArgumentParser(description="Ingest ESG PDF documents")
    parser.add_argument("--input", required=True, help="Path to a PDF file or folder")
    parser.add_argument("--company", required=True, help="Company name, e.g. Infosys")
    parser.add_argument("--ticker", required=True, help="Ticker symbol, e.g. INFY")
    parser.add_argument("--year", required=True, type=int, help="Document year, e.g. 2023")
    parser.add_argument(
        "--document-type",
        required=True,
        help="Document type, e.g. annual_report, brsr, sustainability_report, sample_report",
    )
    parser.add_argument(
        "--pillar",
        default="General",
        help="ESG pillar label: E, S, G, or General",
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_paths = [input_path]
    elif input_path.is_dir():
        pdf_paths = sorted(input_path.glob("*.pdf"))
    else:
        raise ValueError("--input must be a PDF file or a folder containing PDF files")

    if not pdf_paths:
        raise ValueError(f"No PDF files found in {input_path}")

    for pdf_path in pdf_paths:
        print(f"\nIngesting {pdf_path}")
        ingest_pdf(
            pdf_path=str(pdf_path),
            company_name=args.company,
            ticker=args.ticker,
            document_year=args.year,
            document_type=args.document_type,
            esg_pillar=args.pillar,
        )


if __name__ == "__main__":
    main()