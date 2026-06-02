from typing import List, Dict, Any

from normalizer.llm_source_enricher import enrich_source_with_llm


def normalize_all_sources(
    sources: List[Dict[str, Any]],
    query: str = None,
    use_llm_scoring: bool = False
) -> List[Dict[str, Any]]:

    normalized = []

    for source in sources:
        if not source:
            continue

        content = str(source.get("content", "")).strip()

        if len(content) < 20:
            continue

        item = {
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
        }

        if use_llm_scoring and query:
            item = enrich_source_with_llm(
                query=query,
                source=item
            )

        normalized.append(item)

    return normalized