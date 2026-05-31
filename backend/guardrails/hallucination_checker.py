from typing import List, Dict, Any


def filter_supported_sources(
    query: str,
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    supported_sources = []

    query_terms = set(
        query.lower().split()
    )

    for source in sources:
        content = str(
            source.get("content", "")
        ).lower()

        title = str(
            source.get("title", "")
        ).lower()

        if len(content.strip()) < 20:
            continue

        try:
            relevance = float(
                source.get("relevance_score", 0.5)
            )
        except Exception:
            relevance = 0.5

        source_terms = set(
            (content + " " + title).split()
        )

        overlap = query_terms.intersection(source_terms)

        if relevance >= 0.45 or len(overlap) >= 1:
            supported_sources.append(source)

    return supported_sources