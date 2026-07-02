import pytest

from agents.document_ingestor import chunk_text, make_chunk_id


def test_chunk_text_splits_long_text():
    text = "a" * 2000

    chunks = chunk_text(text, chunk_size=800, overlap=100)

    assert len(chunks) == 3
    assert chunks[0] == "a" * 800
    assert chunks[1] == "a" * 800
    assert chunks[2] == "a" * 600


def test_chunk_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("example text", chunk_size=100, overlap=100)


def test_make_chunk_id_is_stable():
    first_id = make_chunk_id(
        source_document="sample.pdf",
        page_number=1,
        chunk_index=0,
        text="same text",
    )
    second_id = make_chunk_id(
        source_document="sample.pdf",
        page_number=1,
        chunk_index=0,
        text="same text",
    )

    assert first_id == second_id


def test_make_chunk_id_changes_when_text_changes():
    first_id = make_chunk_id(
        source_document="sample.pdf",
        page_number=1,
        chunk_index=0,
        text="same text",
    )
    second_id = make_chunk_id(
        source_document="sample.pdf",
        page_number=1,
        chunk_index=0,
        text="different text",
    )

    assert first_id != second_id