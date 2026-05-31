from typing import List, Dict, Any, Optional

from rag.retriever import retrieve_document_context
from normalizer.normalize_document import normalize_document_result
from core.logger import log_error


SUPPORTED_DOCUMENT_TYPES = [
    "pdf",
    "docx",
    "txt",
    "md",
]


def document_agent(
    query: str,
    user_id: str = "anonymous",
    document_id: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Production-level document retrieval agent.

    Supports:
    - PDF
    - DOCX
    - TXT
    - MD
    - OCR-extracted scanned PDFs

    Responsibilities:
    1. Search only user's uploaded documents.
    2. Retrieve relevant chunks from vector DB.
    3. Preserve document metadata.
    4. Normalize results into common source schema.
    5. Return sources only, not final answer.
    """

    if not query or not query.strip():
        return []

    if document_type and document_type not in SUPPORTED_DOCUMENT_TYPES:
        log_error(
            module="document_agent",
            message="Unsupported document type",
            error=document_type
        )
        return []

    try:
        raw_results = retrieve_document_context(
            query=query,
            user_id=user_id,
            document_id=document_id,
            document_type=document_type,
            top_k=top_k
        )

        normalized_results = []

        for item in raw_results:
            normalized = normalize_document_result(item)

            if normalized:
                normalized_results.append(normalized)

        normalized_results = remove_duplicate_document_chunks(
            normalized_results
        )

        normalized_results = sort_document_results(
            normalized_results
        )

        return normalized_results

    except Exception as error:
        log_error(
            module="document_agent",
            message="Document retrieval failed",
            error=str(error)
        )
        return []


def remove_duplicate_document_chunks(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    seen = set()
    unique_sources = []

    for source in sources:
        metadata = source.get("metadata", {})

        key = (
            source.get("source_name", ""),
            source.get("page", ""),
            metadata.get("document_id", ""),
            metadata.get("document_type", ""),
            source.get("content", "")[:150],
        )

        if key in seen:
            continue

        seen.add(key)
        unique_sources.append(source)

    return unique_sources


def sort_document_results(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return sorted(
        sources,
        key=lambda item: (
            float(item.get("trust_score", 0) or 0),
            float(item.get("relevance_score", 0) or 0),
        ),
        reverse=True
    )