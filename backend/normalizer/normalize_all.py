from typing import List, Dict, Any


def normalize_all_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    normalized = []

    for source in sources:
        if not source:
            continue

        content = str(source.get("content", "")).strip()

        if len(content) < 20:
            continue

        normalized.append({
            "source_type": source.get("source_type", "unknown"),
            "source_name": source.get("source_name", "Unknown Source"),
            "title": source.get("title", "Untitled"),
            "content": content,
            "url": source.get("url"),
            "page": source.get("page"),
            "citation": source.get("citation"),
            "court": source.get("court"),
            "date": source.get("date"),
            "language": source.get("language", "en"),
            "trust_score": source.get("trust_score", 0.5),
            "relevance_score": source.get("relevance_score", 0.5),
            "metadata": source.get("metadata", {}),
        })

    return normalized