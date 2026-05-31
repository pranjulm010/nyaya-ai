from typing import Dict, Any, Optional


def normalize_web_result(
    item: Dict[str, Any],
    source_name: str,
    source_type: str = "web",
    trust_score: float = 0.6
) -> Optional[Dict[str, Any]]:

    if not item:
        return None

    title = (
        item.get("title")
        or item.get("name")
        or "Untitled Web Source"
    )

    content = (
        item.get("content")
        or item.get("summary")
        or item.get("description")
        or item.get("snippet")
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
        "page": None,
        "citation": item.get("citation"),
        "court": item.get("court"),
        "date": item.get("date"),
        "language": item.get("language", "en"),
        "trust_score": trust_score,
        "relevance_score": item.get("relevance_score", 0.6),
        "metadata": item.get("metadata", {}),
    }