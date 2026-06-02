from core.llm_router import run_llm


def llm_relevance_score(query: str, title: str, content: str) -> float:
    prompt = f"""
You are a legal search result relevance evaluator.

User query:
{query}

Result title:
{title}

Result content:
{content}

Give relevance score between 0 and 1.

Rules:
- 1.0 = directly answers the legal query
- 0.7 = useful and related
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
        return 0.5


def enrich_result_with_llm(query: str, result: dict) -> dict:
    item = dict(result)

    item["relevance_score"] = llm_relevance_score(
        query=query,
        title=item.get("title", ""),
        content=item.get("content", "")
    )

    return item


def sort_and_limit_results(results: list, max_results: int = 5) -> list:
    return sorted(
        results,
        key=lambda x: x.get("relevance_score", 0),
        reverse=True
    )[:max_results]