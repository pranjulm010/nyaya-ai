from typing import Dict, Any
from core.llm_router import run_llm


def llm_relevance_score(query: str, source: Dict[str, Any]) -> float:
    """
    Uses LLM only to judge semantic relevance.
    Normalization itself remains rule-based.
    """

    if not query or not source:
        return float(source.get("relevance_score", 0.5))

    content = str(source.get("content", ""))[:2500]
    title = str(source.get("title", ""))

    prompt = f"""
You are a legal source relevance scorer.

User question:
{query}

Source title:
{title}

Source content:
{content}

Give relevance score between 0 and 1.

Rules:
- 1.0 = directly answers the legal question
- 0.7 = useful but partial
- 0.4 = weakly related
- 0.0 = unrelated

Return only a number.
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="legal_research",
            temperature=0
        )

        score = float(result.strip())

        if score < 0:
            return 0.0

        if score > 1:
            return 1.0

        return round(score, 3)

    except Exception:
        return float(source.get("relevance_score", 0.5))


def enrich_source_with_llm(
    query: str,
    source: Dict[str, Any]
) -> Dict[str, Any]:
    item = dict(source)

    item["relevance_score"] = llm_relevance_score(
        query=query,
        source=item
    )

    return item