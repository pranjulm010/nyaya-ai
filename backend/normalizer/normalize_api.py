from typing import Dict, Any, Optional


def normalize_api_result(
    item: Dict[str, Any],
    source_name: str,
    source_type: str = "api",
    trust_score: float = 0.75
) -> Optional[Dict[str, Any]]:

    if not item:
        return None

    title = (
        item.get("title")
        or item.get("case_title")
        or item.get("name")
        or "Untitled Legal Source"
    )

    content = (
        item.get("content")
        or item.get("headline")
        or item.get("summary")
        or item.get("description")
        or item.get("snippet")
        or item.get("text")
        or ""
    )

    if not content and not title:
        return None

    return {
        "source_type": source_type,
        "source_name": source_name,
        "title": title,
        "content": content,
        "url": item.get("url"),
        "page": item.get("page"),
        "citation": item.get("citation"),
        "court": item.get("court") or item.get("docsource"),
        "date": item.get("date") or item.get("publishdate"),
        "language": item.get("language", "en"),
        "trust_score": trust_score,
        "relevance_score": item.get("relevance_score", 0.7),
        "metadata": item.get("metadata", {}),
    }