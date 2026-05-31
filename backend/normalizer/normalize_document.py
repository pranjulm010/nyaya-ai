from typing import Dict, Any, Optional


def normalize_document_result(
    item: Dict[str, Any]
) -> Optional[Dict[str, Any]]:

    if not item:
        return None

    content = str(item.get("content", "")).strip()

    if len(content) < 20:
        return None

    document_type = item.get("document_type", "unknown")

    trust_score = 0.95

    if document_type in ["txt", "md"]:
        trust_score = 0.80

    return {
        "source_type": "document",
        "source_name": item.get("source", "Uploaded Document"),
        "title": item.get("title") or item.get("source", "Uploaded Document"),
        "content": content,
        "url": None,
        "page": item.get("page"),
        "citation": None,
        "court": None,
        "date": None,
        "language": item.get("language", "en"),
        "trust_score": trust_score,
        "relevance_score": item.get("score", 0.7),
        "metadata": {
            "document_id": item.get("document_id"),
            "user_id": item.get("user_id"),
            "document_type": document_type,
            "total_pages": item.get("total_pages"),
            "chunk_id": item.get("chunk_id"),
        }
    }