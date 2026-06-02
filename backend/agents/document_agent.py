from typing import List, Dict, Any, Optional

from rag.retriever import retrieve_document_context
from normalizer.normalize_document import normalize_document_result
from core.logger import log_error

SUPPORTED_DOCUMENT_TYPES = ["pdf", "docx", "txt", "md"]


def document_agent(query: str, user_id: str = "anonymous", document_id: Optional[str] = None, document_type: Optional[str] = None, top_k: int = 8) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []

    if document_type:
        document_type = document_type.lower().strip()
        if document_type not in SUPPORTED_DOCUMENT_TYPES:
            log_error("document_agent", "Unsupported document type", document_type)
            return []

    try:
        raw_results = retrieve_document_context(query=query, user_id=user_id, document_id=document_id, document_type=document_type, top_k=top_k)
        normalized_results = []
        for item in raw_results or []:
            normalized = normalize_document_result(item)
            if normalized:
                normalized.setdefault("source_type", "document")
                normalized.setdefault("trust_score", 0.93)
                normalized_results.append(normalized)
        return sort_document_results(remove_duplicate_document_chunks(normalized_results))
    except Exception as error:
        log_error("document_agent", "Document retrieval failed", str(error))
        return []


def remove_duplicate_document_chunks(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique_sources = []
    for source in sources:
        metadata = source.get("metadata", {}) or {}
        key = (
            source.get("source_name", ""),
            source.get("page", ""),
            metadata.get("document_id", ""),
            metadata.get("document_type", ""),
            str(source.get("content", ""))[:180].lower().strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique_sources.append(source)
    return unique_sources


def sort_document_results(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(sources, key=lambda item: (float(item.get("trust_score", 0) or 0), float(item.get("relevance_score", 0) or 0)), reverse=True)
