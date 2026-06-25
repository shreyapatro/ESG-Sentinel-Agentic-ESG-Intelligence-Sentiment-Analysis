import argparse
from pathlib import Path
from models.embeddings import embed_texts
from rag.vector_store import store_document_chunks
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
    parser.add_argument("--input", required=True, help="Path to a PDF file")
    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        ingest_pdf(str(input_path))
    else:
        raise ValueError("For now, --input must be a single PDF file")


if __name__ == "__main__":
    main()