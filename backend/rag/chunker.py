from typing import List, Dict, Any


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[str]:

    if not text or not text.strip():
        print("CHUNKER: empty text received")
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    print("CHUNKER TOTAL:", len(chunks))

    if chunks:
        print("FIRST CHUNK PREVIEW:")
        print(chunks[0][:500])

    return chunks


def create_chunks_with_metadata(
    text: str,
    metadata: Dict[str, Any],
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[Dict[str, Any]]:

    chunks = chunk_text(
        text=text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    final_chunks = []

    document_id = metadata.get(
        "document_id",
        "unknown_document"
    )

    for index, chunk in enumerate(chunks):
        item = dict(metadata)
        item["content"] = chunk
        item["chunk_id"] = f"{document_id}_{index}"

        final_chunks.append(item)

    print(
        "CHUNKER METADATA CHUNKS:",
        len(final_chunks)
    )

    return final_chunks