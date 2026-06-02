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
from core.llm_router import run_llm
from core.logger import log_error


WEB_CONNECTORS = [
    {
        "name": "Supreme Court of India",
        "function": scrape_supreme_court,
        "type": "official",
        "trust_score": 0.96,
    },
    {
        "name": "High Courts",
        "function": scrape_high_courts,
        "type": "official",
        "trust_score": 0.92,
    },
    {
        "name": "India Code",
        "function": scrape_india_code,
        "type": "official",
        "trust_score": 0.96,
    },
    {
        "name": "PRS India",
        "function": scrape_prs_india,
        "type": "web",
        "trust_score": 0.80,
    },
    {
        "name": "LiveLaw",
        "function": scrape_live_law,
        "type": "web",
        "trust_score": 0.70,
    },
    {
        "name": "Bar and Bench",
        "function": scrape_bar_and_bench,
        "type": "web",
        "trust_score": 0.70,
    },
    {
        "name": "Generic Web",
        "function": scrape_generic_web,
        "type": "web",
        "trust_score": 0.45,
    },
]


def web_agent(
    query: str,
    max_results_per_site: int = 3,
    max_workers: int = 4,
    force_all_sources: bool = False
) -> List[Dict[str, Any]]:

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

    if force_all_sources:
        return WEB_CONNECTORS

    connector_names = [
        connector["name"]
        for connector in WEB_CONNECTORS
    ]

    prompt = f"""
You are an Indian legal web source selector.

User query:
{query}

Available web connectors:
{connector_names}

Choose the most useful sources.

Source meaning:
- Supreme Court of India: official Supreme Court website.
- High Courts: official High Court websites.
- India Code: official statutes and bare acts.
- PRS India: bills, amendments, policy, parliament.
- LiveLaw: recent legal news and judgments.
- Bar and Bench: recent legal news and judgments.
- Generic Web: fallback broad web search.

Return only source names separated by commas.
Do not explain.

Rules:
- For latest/current/recent legal news, include LiveLaw and Bar and Bench.
- For statutes/sections/articles, include India Code.
- For judgments/cases, include Supreme Court of India, High Courts, and Generic Web if useful.
- If unsure, return:
India Code, PRS India, Generic Web
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="legal_research",
            temperature=0
        )

        selected_names = {
            name.strip()
            for name in result.split(",")
            if name.strip()
        }

        selected = [
            connector
            for connector in WEB_CONNECTORS
            if connector["name"] in selected_names
        ]

        if selected:
            return selected

        return default_web_connectors()

    except Exception as error:
        log_error(
            module="web_agent",
            message="LLM web connector selection failed",
            error=str(error)
        )
        return default_web_connectors()


def default_web_connectors() -> List[Dict[str, Any]]:
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
    title = str(source.get("title", "")).lower().strip()
    url = str(source.get("url", "")).lower().strip()
    source_name = str(source.get("source_name", "")).lower().strip()

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