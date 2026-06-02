from typing import List, Dict, Any
from core.llm_router import run_llm


def rank_sources(sources, query):

    scored = []

    for source in sources:
        content = source.get("content", "")[:2000]

        prompt = f"""
Question:
{query}

Source:
{content}

Give relevance score from 0 to 1.

Return number only.
"""

        try:
            score = run_llm(
                prompt=prompt,
                intent="legal_research",
                temperature=0
            )

            score = float(score.strip())

        except Exception:
            score = 0.5

        source["final_score"] = score
        scored.append(source)

    return sorted(
        scored,
        key=lambda x: x["final_score"],
        reverse=True
    )