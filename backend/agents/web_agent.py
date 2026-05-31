import concurrent.futures
from typing import List, Dict, Any

from sources.supreme_court import scrape_supreme_court
from sources.high_courts import scrape_high_courts
from sources.india_code import scrape_india_code
from sources.prs_india import scrape_prs_india
from sources.live_law import scrape_live_law
from sources.bar_and_bench import scrape_bar_and_bench
from sources.generic_web import scrape_generic_web

from normalizer.normalize_web import normalize_web_result
from core.logger import log_error


WEB_CONNECTORS = [
    {
        "name": "Supreme Court of India",
        "function": scrape_supreme_court,
        "type": "official",
        "trust_score": 0.96,
        "keywords": [
            "supreme court", "judgment", "judgement", "order",
            "appeal", "sci", "constitution bench"
        ],
    },
    {
        "name": "High Courts",
        "function": scrape_high_courts,
        "type": "official",
        "trust_score": 0.92,
        "keywords": [
            "high court", "writ", "petition", "state",
            "bail", "order", "judgment"
        ],
    },
    {
        "name": "India Code",
        "function": scrape_india_code,
        "type": "official",
        "trust_score": 0.96,
        "keywords": [
            "section", "article", "act", "law", "ipc", "crpc",
            "bns", "bnss", "constitution", "provision", "rule",
            "bare act"
        ],
    },
    {
        "name": "PRS India",
        "function": scrape_prs_india,
        "type": "web",
        "trust_score": 0.80,
        "keywords": [
            "bill", "amendment", "policy", "parliament",
            "act summary", "legislative", "law reform"
        ],
    },
    {
        "name": "LiveLaw",
        "function": scrape_live_law,
        "type": "web",
        "trust_score": 0.70,
        "keywords": [
            "latest", "recent", "today", "news", "update",
            "judgment", "court", "supreme court", "high court"
        ],
    },
    {
        "name": "Bar and Bench",
        "function": scrape_bar_and_bench,
        "type": "web",
        "trust_score": 0.70,
        "keywords": [
            "latest", "recent", "today", "news", "update",
            "judgment", "court", "supreme court", "high court"
        ],
    },
    {
        "name": "Generic Web",
        "function": scrape_generic_web,
        "type": "web",
        "trust_score": 0.45,
        "keywords": [],
    },
]


def web_agent(
    query: str,
    max_results_per_site: int = 3,
    max_workers: int = 4,
    force_all_sources: bool = False
) -> List[Dict[str, Any]]:
    """
    Production-level multi-website legal web agent.

    Rules:
    1. Never depend on one website.
    2. Prefer official court/government/legal sources.
    3. Use legal news only for recent/current context.
    4. Use generic web only as fallback.
    5. If one website fails, continue with others.
    6. Return normalized source objects only.
    """

    if not query or not query.strip():
        return []

    selected_connectors = select_web_connectors(
        query=query,
        force_all_sources=force_all_sources
    )

    all_results: List[Dict[str, Any]] = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_map = {
            executor.submit(
                call_web_connector,
                connector,
                query,
                max_results_per_site
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
                    module="web_agent",
                    message=f"{connector['name']} future failed",
                    error=str(error)
                )

    all_results = remove_duplicate_web_sources(all_results)
    all_results = sort_web_results(all_results)

    return all_results


def select_web_connectors(
    query: str,
    force_all_sources: bool = False
) -> List[Dict[str, Any]]:
    """
    Cost-optimized website selection.

    It avoids scraping every website for every query.
    """

    if force_all_sources:
        return WEB_CONNECTORS

    q = query.lower()

    selected = []

    for connector in WEB_CONNECTORS:
        keywords = connector.get("keywords", [])

        if keywords and any(keyword in q for keyword in keywords):
            selected.append(connector)

    if selected:
        return selected

    return default_web_connectors()


def default_web_connectors() -> List[Dict[str, Any]]:
    """
    Safe fallback for general legal questions.
    Generic Web is included only as fallback.
    """

    default_names = {
        "India Code",
        "PRS India",
        "Generic Web",
    }

    return [
        connector
        for connector in WEB_CONNECTORS
        if connector["name"] in default_names
    ]


def call_web_connector(
    connector: Dict[str, Any],
    query: str,
    max_results: int
) -> List[Dict[str, Any]]:
    """
    Calls one website connector safely.
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
            normalized = normalize_web_result(
                item=item,
                source_name=connector["name"],
                source_type=connector["type"],
                trust_score=connector["trust_score"],
            )

            if normalized:
                normalized_results.append(normalized)

        return normalized_results

    except Exception as error:
        log_error(
            module="web_agent",
            message=f"{connector['name']} connector error",
            error=str(error)
        )
        return []


def remove_duplicate_web_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
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

    source_name = str(
        source.get("source_name", "")
    ).lower().strip()

    return f"{source_name}|{title}|{url}"


def sort_web_results(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return sorted(
        sources,
        key=lambda item: (
            float(item.get("trust_score", 0) or 0),
            float(item.get("relevance_score", 0) or 0),
        ),
        reverse=True
    )