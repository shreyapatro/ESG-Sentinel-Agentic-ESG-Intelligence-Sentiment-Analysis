import argparse
from pathlib import Path

from agents.document_ingestor import build_document_chunks, extract_pdf_pages


def ingest_pdf(pdf_path: str) -> None:
    pages = extract_pdf_pages(pdf_path)

    chunks = build_document_chunks(
        pages=pages,
        company_name="Infosys",
        ticker="INFY",
        document_year=2023,
        document_type="sample_report",
        esg_pillar="General",
    )

    print(f"Extracted {len(pages)} pages from {pdf_path}")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks[:3]:
        preview = chunk["text"][:200].replace("\n", " ")
        print(f"\nChunk {chunk['chunk_id']}")
        print(f"Company: {chunk['company_name']} | Page: {chunk['page_number']}")
        print(preview)


def main():
    parser = argparse.ArgumentParser(description="Ingest ESG PDF documents")
    parser.add_argument("--input", required=True, help="Path to a PDF file")
    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        ingest_pdf(str(input_path))
    else:
        raise ValueError("For now, --input must be a single PDF file")


if __name__ == "__main__":
    main()