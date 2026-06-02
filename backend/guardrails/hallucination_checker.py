from typing import List, Dict, Any
from core.llm_router import run_llm


def filter_supported_sources(
    query: str,
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    supported = []

    for source in sources:
        content = str(source.get("content", ""))

        if len(content.strip()) < 20:
            continue

        prompt = f"""
You are a legal grounding evaluator.

Question:
{query}

Source:
{content[:3000]}

Can this source help answer the question?

Return only:
SUPPORTED
or
NOT_SUPPORTED
"""

        try:
            result = run_llm(
                prompt=prompt,
                intent="legal_research",
                temperature=0
            )

            if result.strip().upper() == "SUPPORTED":
                supported.append(source)

        except Exception:
            continue

    return supported