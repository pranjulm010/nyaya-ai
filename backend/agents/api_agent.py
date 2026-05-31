import concurrent.futures
from typing import List, Dict, Any

from sources.indian_kanoon import search_indian_kanoon
from sources.ecourts import search_ecourts
from sources.supreme_court import search_supreme_court
from sources.high_courts import search_high_courts
from sources.india_code import search_india_code
from sources.prs_india import search_prs_india

from normalizer.normalize_api import normalize_api_result
from core.logger import log_error


API_CONNECTORS = [
    {
        "name": "India Code",
        "function": search_india_code,
        "priority": 0.98,
        "type": "official",
        "keywords": [
            "section", "act", "law", "ipc", "crpc", "bns",
            "bnss", "constitution", "article", "provision",
            "rule", "bare act"
        ],
    },
    {
        "name": "Supreme Court of India",
        "function": search_supreme_court,
        "priority": 0.96,
        "type": "official",
        "keywords": [
            "supreme court", "judgment", "judgement",
            "case", "citation", "precedent", "appeal",
            "article", "constitutional"
        ],
    },
    {
        "name": "High Courts",
        "function": search_high_courts,
        "priority": 0.92,
        "type": "official",
        "keywords": [
            "high court", "writ", "bail", "petition",
            "state", "judgment", "case", "order"
        ],
    },
    {
        "name": "Indian Kanoon",
        "function": search_indian_kanoon,
        "priority": 0.86,
        "type": "api",
        "keywords": [
            "case", "judgment", "judgement", "citation",
            "court", "bail", "petition", "precedent",
            "section", "ipc", "crpc", "bns", "bnss"
        ],
    },
    {
        "name": "eCourts",
        "function": search_ecourts,
        "priority": 0.84,
        "type": "api",
        "keywords": [
            "case status", "cnr", "court status",
            "hearing", "next date", "case number",
            "filing number"
        ],
    },
    {
        "name": "PRS India",
        "function": search_prs_india,
        "priority": 0.78,
        "type": "api",
        "keywords": [
            "bill", "amendment", "policy", "parliament",
            "act summary", "law reform", "legislative"
        ],
    },
]


def api_agent(
    query: str,
    max_results_per_source: int = 5,
    max_workers: int = 4,
    force_all_sources: bool = False
) -> List[Dict[str, Any]]:
    """
    Production-level multi-source API agent.

    It does not depend on one API.

    Responsibilities:
    1. Select relevant legal API connectors.
    2. Query multiple sources in parallel.
    3. Continue even if one API fails.
    4. Normalize every response into common source schema.
    5. Remove duplicate results.
    6. Sort by trust + relevance.
    7. Return sources only, not final answer.
    """

    if not query or not query.strip():
        return []

    selected_connectors = select_connectors(
        query=query,
        force_all_sources=force_all_sources
    )

    all_results: List[Dict[str, Any]] = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_map = {
            executor.submit(
                call_connector,
                connector,
                query,
                max_results_per_source
            ): connector
            for connector in selected_connectors
        }

        for future in concurrent.futures.as_completed(future_map):
            connector = future_map[future]

            try:
                results = future.result()
                all_results.extend(results)

            except Exception as error:
                log_error(
                    module="api_agent",
                    message=f"{connector['name']} future failed",
                    error=str(error)
                )

    all_results = remove_duplicate_sources(all_results)
    all_results = sort_api_results(all_results)

    return all_results


def select_connectors(
    query: str,
    force_all_sources: bool = False
) -> List[Dict[str, Any]]:
    """
    Cost-optimized connector selection.

    Instead of calling every API every time,
    this selects only useful APIs.

    If no connector matches, it uses a safe fallback.
    """

    if force_all_sources:
        return API_CONNECTORS

    q = query.lower()

    selected = []

    for connector in API_CONNECTORS:
        keywords = connector.get("keywords", [])

        if any(keyword in q for keyword in keywords):
            selected.append(connector)

    if selected:
        return selected

    return default_connectors_for_general_legal_query()


def default_connectors_for_general_legal_query() -> List[Dict[str, Any]]:
    """
    Cheap fallback for normal public legal questions.
    """

    default_names = {
        "India Code",
        "Indian Kanoon",
        "PRS India",
    }

    return [
        connector
        for connector in API_CONNECTORS
        if connector["name"] in default_names
    ]


def call_connector(
    connector: Dict[str, Any],
    query: str,
    max_results: int
) -> List[Dict[str, Any]]:
    """
    Calls one source connector safely.
    """

    try:
        raw_results = connector["function"](
            query=query,
            max_results=max_results
        )

        if not raw_results:
            return []

        normalized_results = []

        for item in raw_results:
            normalized = normalize_api_result(
                item=item,
                source_name=connector["name"],
                source_type=connector["type"],
                trust_score=connector["priority"],
            )

            if normalized:
                normalized_results.append(normalized)

        return normalized_results

    except Exception as error:
        log_error(
            module="api_agent",
            message=f"{connector['name']} failed",
            error=str(error)
        )
        return []


def remove_duplicate_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Removes duplicate legal results across APIs.
    """

    seen = set()
    unique_sources = []

    for source in sources:
        key = build_duplicate_key(source)

        if key in seen:
            continue

        seen.add(key)
        unique_sources.append(source)

    return unique_sources


def build_duplicate_key(source: Dict[str, Any]) -> str:
    title = str(
        source.get("title", "")
    ).lower().strip()

    url = str(
        source.get("url", "")
    ).lower().strip()

    citation = str(
        source.get("citation", "")
    ).lower().strip()

    court = str(
        source.get("court", "")
    ).lower().strip()

    date = str(
        source.get("date", "")
    ).lower().strip()

    return f"{title}|{url}|{citation}|{court}|{date}"


def sort_api_results(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Sorts sources by trust and relevance.
    """

    return sorted(
        sources,
        key=lambda item: (
            float(item.get("trust_score", 0) or 0),
            float(item.get("relevance_score", 0) or 0),
        ),
        reverse=True
    )