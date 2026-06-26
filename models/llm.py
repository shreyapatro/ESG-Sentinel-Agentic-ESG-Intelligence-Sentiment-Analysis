import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def build_context(retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]
        source = metadata["source_document"]
        page = metadata["page_number"]
        text = chunk["text"]

        context_blocks.append(
            f"""
            Evidence {index}
            source_document: {source}
            page_number: {page}
            text:
            {text}
            """.strip()
        )

    return "\n\n".join(context_blocks)


def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

    context = build_context(retrieved_chunks)

    prompt = f"""
You are ESG Sentinel, an ESG research assistant.

Answer the user's question using only the evidence below.

Rules:
- Use only the provided evidence.
- If the evidence is insufficient, say that the available evidence is insufficient.
- Every factual claim must include a citation.
- Citation format must be exactly: (source_document, page X)
- Replace source_document with the actual filename from the evidence.
- Do not cite as Evidence 1, Evidence 2, [1], or [2].
- Keep the answer concise and factual.

Question:
{question}

Evidence:
{context}
"""

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You answer ESG questions using provided evidence and citations.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content