import concurrent.futures
import json
import re
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
    {"name": "Supreme Court of India", "function": scrape_supreme_court, "type": "official", "trust_score": 0.96, "description": "Official Supreme Court judgments and orders."},
    {"name": "High Courts", "function": scrape_high_courts, "type": "official", "trust_score": 0.92, "description": "Official High Court judgments, orders and writs."},
    {"name": "India Code", "function": scrape_india_code, "type": "official", "trust_score": 0.96, "description": "Official statutes, bare acts and provisions."},
    {"name": "PRS India", "function": scrape_prs_india, "type": "web", "trust_score": 0.80, "description": "Bills, amendments, parliament and policy summaries."},
    {"name": "LiveLaw", "function": scrape_live_law, "type": "web", "trust_score": 0.70, "description": "Recent legal news, judgments and legal updates."},
    {"name": "Bar and Bench", "function": scrape_bar_and_bench, "type": "web", "trust_score": 0.70, "description": "Recent court news, legal updates and judgments."},
    {"name": "Generic Web", "function": scrape_generic_web, "type": "web", "trust_score": 0.45, "description": "Fallback broad search for public legal pages."},
]


def web_agent(query: str, max_results_per_site: int = 3, max_workers: int = 4, force_all_sources: bool = False) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []
    selected_connectors = select_web_connectors(query=query, force_all_sources=force_all_sources)
    if not selected_connectors:
        selected_connectors = default_web_connectors()

    all_results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(call_web_connector, connector, query, max_results_per_site): connector for connector in selected_connectors}
        for future in concurrent.futures.as_completed(future_map):
            connector = future_map[future]
            try:
                all_results.extend(future.result())
            except Exception as error:
                log_error("web_agent", f"{connector['name']} future failed", str(error))
    return sort_web_results(remove_duplicate_web_sources(all_results))


def select_web_connectors(query: str, force_all_sources: bool = False) -> List[Dict[str, Any]]:
    if force_all_sources:
        return WEB_CONNECTORS

    prompt = f"""
You are Nyaya AI's Indian legal website source selector.
Select website connectors by understanding the query, not by keyword matching.

User query:
{query}

Available website connectors:
{json.dumps([{k: c[k] for k in ['name', 'description']} for c in WEB_CONNECTORS], ensure_ascii=False)}

Return ONLY valid JSON:
{{"sources": ["source name"], "reason": "short reason"}}

Rules:
- For latest/current/recent developments, include LiveLaw, Bar and Bench and Generic Web.
- For statutes/articles/sections, include India Code.
- For judgments/cases, include Supreme Court of India, High Courts and Generic Web.
- For bills/amendments/policy, include PRS India and India Code.
- If PDF context is present in the query, include official court/statute sites and Generic Web for verification.
- If unsure, return India Code, Supreme Court of India, Generic Web.
- Select 2 to 5 sources.
"""
    try:
        raw = run_llm(prompt=prompt, intent="legal_research", temperature=0)
        data = parse_json_safely(raw)
        selected_names = set(data.get("sources", []))
        selected = [c for c in WEB_CONNECTORS if c["name"] in selected_names]
        return selected or default_web_connectors()
    except Exception as error:
        log_error("web_agent", "LLM web connector selection failed", str(error))
        return default_web_connectors()


def parse_json_safely(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except Exception:
        return {}


def default_web_connectors() -> List[Dict[str, Any]]:
    names = {"India Code", "Supreme Court of India", "Generic Web"}
    return [c for c in WEB_CONNECTORS if c["name"] in names]


def call_web_connector(connector: Dict[str, Any], query: str, max_results: int) -> List[Dict[str, Any]]:
    try:
        raw_results = connector["function"](query=query, max_results=max_results)
        normalized_results = []
        for item in raw_results or []:
            normalized = normalize_web_result(item=item, source_name=connector["name"], source_type=connector["type"], trust_score=connector["trust_score"])
            if normalized:
                normalized_results.append(normalized)
        return normalized_results
    except Exception as error:
        log_error("web_agent", f"{connector['name']} connector error", str(error))
        return []


def remove_duplicate_web_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
    return "|".join([str(source.get("source_name", "")).lower().strip(), str(source.get("title", "")).lower().strip(), str(source.get("url", "")).lower().strip()])


def sort_web_results(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(sources, key=lambda item: (float(item.get("trust_score", 0) or 0), float(item.get("relevance_score", 0) or 0)), reverse=True)
