from typing import List, Dict, Any

from guardrails.pii_filter import mask_pii
from guardrails.source_ranker import rank_sources
from guardrails.citation_checker import citation_checker
from guardrails.hallucination_checker import filter_supported_sources
from guardrails.unsafe_advice_blocker import is_unsafe_query
from guardrails.confidence_score import calculate_confidence
from guardrails.legal_disclaimer import legal_disclaimer
from core.logger import log_error


def guardrail_agent(
    query: str,
    sources: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Production-level guardrail agent.

    Responsibilities:
    1. Block unsafe legal misuse.
    2. Mask PII from query and sources.
    3. Remove weak/empty sources.
    4. Rank sources by trust and relevance.
    5. Verify citation anchors.
    6. Keep only source-supported context.
    7. Return safe payload for final_answer_agent.
    """

    try:
        safe_query = mask_pii(query)

        if is_unsafe_query(safe_query):
            return blocked_response(safe_query)

        sanitized_sources = sanitize_sources(sources)

        if not sanitized_sources:
            return no_source_response(safe_query)

        ranked_sources = rank_sources(sanitized_sources)

        citation_checked_sources = citation_checker(ranked_sources)

        supported_sources = filter_supported_sources(
            query=safe_query,
            sources=citation_checked_sources
        )

        if not supported_sources:
            return no_source_response(safe_query)

        confidence = calculate_confidence(supported_sources)

        return {
            "blocked": False,
            "safe_query": safe_query,
            "safe_sources": supported_sources,
            "confidence": confidence,
            "disclaimer": legal_disclaimer(),
            "message": "Guardrail validation completed."
        }

    except Exception as error:
        log_error(
            module="guardrail_agent",
            message="Guardrail validation failed",
            error=str(error)
        )

        return {
            "blocked": False,
            "safe_query": mask_pii(query),
            "safe_sources": [],
            "confidence": "Low",
            "disclaimer": legal_disclaimer(),
            "message": "Guardrail validation failed."
        }


def sanitize_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    clean_sources = []

    for source in sources:
        if not source:
            continue

        content = str(source.get("content", "")).strip()

        if len(content) < 20:
            continue

        clean_source = dict(source)

        clean_source["content"] = mask_pii(content)
        clean_source["title"] = mask_pii(
            str(clean_source.get("title", ""))
        )
        clean_source["source_name"] = mask_pii(
            str(clean_source.get("source_name", ""))
        )

        clean_sources.append(clean_source)

    return clean_sources


def blocked_response(query: str) -> Dict[str, Any]:
    return {
        "blocked": True,
        "safe_query": query,
        "safe_sources": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
        "reason": "unsafe_legal_request",
        "message": (
            "I cannot help with hiding evidence, forging documents, "
            "misleading the court, evading law, bribery, witness tampering, "
            "or misuse of legal process."
        )
    }


def no_source_response(query: str) -> Dict[str, Any]:
    return {
        "blocked": False,
        "safe_query": query,
        "safe_sources": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
        "reason": "no_verified_sources",
        "message": "No reliable verified source context was available."
    }