import concurrent.futures
import json
import re
from typing import List, Dict, Any

from sources.indian_kanoon import search_indian_kanoon
from sources.ecourts import search_ecourts
from sources.supreme_court import search_supreme_court
from sources.high_courts import search_high_courts
from sources.india_code import search_india_code
from sources.prs_india import search_prs_india
from normalizer.normalize_api import normalize_api_result
from core.llm_router import run_llm
from core.logger import log_error

API_CONNECTORS = [
    {"name": "India Code", "function": search_india_code, "priority": 0.98, "type": "official", "description": "Official Indian statutes, bare acts, sections, articles, rules and provisions."},
    {"name": "Supreme Court of India", "function": search_supreme_court, "priority": 0.96, "type": "official", "description": "Official Supreme Court judgments, orders, precedents and constitutional cases."},
    {"name": "High Courts", "function": search_high_courts, "priority": 0.92, "type": "official", "description": "Official High Court judgments, writs, bail orders, state court decisions and petitions."},
    {"name": "Indian Kanoon", "function": search_indian_kanoon, "priority": 0.86, "type": "api", "description": "Searchable Indian case law, judgments, citations and legal precedents."},
    {"name": "eCourts", "function": search_ecourts, "priority": 0.84, "type": "api", "description": "Case status, CNR, hearing date, filing number and next-date style queries."},
    {"name": "PRS India", "function": search_prs_india, "priority": 0.78, "type": "api", "description": "Bills, amendments, parliament, legislative summaries, policy and law reform."},
]


def api_agent(query: str, max_results_per_source: int = 5, max_workers: int = 4, force_all_sources: bool = False) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []

    selected_connectors = select_connectors(query=query, force_all_sources=force_all_sources)
    if not selected_connectors:
        selected_connectors = default_connectors_for_general_legal_query()

    all_results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(call_connector, connector, query, max_results_per_source): connector
            for connector in selected_connectors
        }
        for future in concurrent.futures.as_completed(future_map):
            connector = future_map[future]
            try:
                all_results.extend(future.result())
            except Exception as error:
                log_error("api_agent", f"{connector['name']} future failed", str(error))

    return sort_api_results(remove_duplicate_sources(all_results))


def select_connectors(query: str, force_all_sources: bool = False) -> List[Dict[str, Any]]:
    if force_all_sources:
        return API_CONNECTORS

    prompt = f"""
You are Nyaya AI's Indian legal API source selector.
Select the best API connectors for the user's legal query.

User query:
{query}

Available connectors:
{json.dumps([{k: c[k] for k in ['name', 'description']} for c in API_CONNECTORS], ensure_ascii=False)}

Return ONLY valid JSON:
{{"sources": ["source name"], "reason": "short reason"}}

Rules:
- Do not use keyword matching.
- For normal legal questions, include India Code and Indian Kanoon.
- For case law, include Supreme Court of India, High Courts and Indian Kanoon.
- For statutes/articles/sections, include India Code and Indian Kanoon.
- For case status/CNR/hearing dates, include eCourts.
- For bills/amendments/policy, include PRS India and India Code.
- If the uploaded PDF context is present inside the query, select sources that can verify or supplement it.
- If unsure, return India Code, Indian Kanoon, Supreme Court of India.
- Select 2 to 5 sources, unless the query clearly needs all.
"""
    try:
        raw = run_llm(prompt=prompt, intent="legal_research", temperature=0)
        data = parse_json_safely(raw)
        selected_names = set(data.get("sources", []))
        selected = [c for c in API_CONNECTORS if c["name"] in selected_names]
        return selected or default_connectors_for_general_legal_query()
    except Exception as error:
        log_error("api_agent", "LLM API connector selection failed", str(error))
        return default_connectors_for_general_legal_query()


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


def default_connectors_for_general_legal_query() -> List[Dict[str, Any]]:
    names = {"India Code", "Indian Kanoon", "Supreme Court of India"}
    return [c for c in API_CONNECTORS if c["name"] in names]


def call_connector(connector: Dict[str, Any], query: str, max_results: int) -> List[Dict[str, Any]]:
    try:
        raw_results = connector["function"](query=query, max_results=max_results)
        normalized_results = []
        for item in raw_results or []:
            normalized = normalize_api_result(item=item, source_name=connector["name"], source_type=connector["type"], trust_score=connector["priority"])
            if normalized:
                normalized_results.append(normalized)
        return normalized_results
    except Exception as error:
        log_error("api_agent", f"{connector['name']} failed", str(error))
        return []


def remove_duplicate_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
    return "|".join([
        str(source.get("title", "")).lower().strip(),
        str(source.get("url", "")).lower().strip(),
        str(source.get("citation", "")).lower().strip(),
        str(source.get("court", "")).lower().strip(),
        str(source.get("date", "")).lower().strip(),
    ])


def sort_api_results(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(sources, key=lambda item: (float(item.get("trust_score", 0) or 0), float(item.get("relevance_score", 0) or 0)), reverse=True)
