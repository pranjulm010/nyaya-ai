from typing import List, Dict, Any


def calculate_confidence(
    sources: List[Dict[str, Any]]
) -> str:

    if not sources:
        return "Low"

    scores = []

    for source in sources:
        score = (
            source.get("final_score")
            or source.get("relevance_score")
            or source.get("trust_score")
            or 0
        )

        try:
            scores.append(float(score))
        except Exception:
            continue

    if not scores:
        return "Low"

    avg_score = sum(scores) / len(scores)

    strong_source_count = sum(
        1
        for source in sources
        if source.get("source_type") in [
            "document",
            "pdf",
            "official",
        ]
    )

    if avg_score >= 0.8 and strong_source_count >= 1:
        return "High"

    if avg_score >= 0.6:
        return "Medium"

    return "Low"