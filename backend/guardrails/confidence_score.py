from typing import List, Dict, Any
from core.llm_router import run_llm


def calculate_confidence(
    sources: List[Dict[str, Any]]
) -> str:

    if not sources:
        return "Low"

    source_summary = []

    for s in sources:
        source_summary.append({
            "type": s.get("source_type"),
            "score": s.get("final_score"),
            "title": s.get("title")
        })

    prompt = f"""
Evaluate legal answer confidence.

Sources:
{source_summary}

Return only:
HIGH
MEDIUM
LOW
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="simple_legal",
            temperature=0
        )

        result = result.strip().capitalize()

        if result in ["High", "Medium", "Low"]:
            return result

        return "Medium"

    except Exception:
        return "Low"