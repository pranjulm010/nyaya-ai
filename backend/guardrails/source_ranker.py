from typing import List, Dict, Any


SOURCE_PRIORITY = {
    "document": 0.95,
    "pdf": 0.95,
    "official": 0.92,
    "api": 0.82,
    "web": 0.60,
    "memory": 0.40,
}


def rank_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    ranked = []

    for source in sources:
        item = dict(source)

        source_type = item.get("source_type", "web")

        trust_score = float(
            item.get("trust_score")
            or SOURCE_PRIORITY.get(source_type, 0.5)
        )

        relevance_score = float(
            item.get("relevance_score")
            or 0.5
        )

        final_score = round(
            (trust_score * 0.6) + (relevance_score * 0.4),
            3
        )

        item["trust_score"] = trust_score
        item["relevance_score"] = relevance_score
        item["final_score"] = final_score

        ranked.append(item)

    return sorted(
        ranked,
        key=lambda x: x.get("final_score", 0),
        reverse=True
    )