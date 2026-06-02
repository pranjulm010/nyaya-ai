from typing import List, Dict, Any

from guardrails.pii_filter import mask_pii
from guardrails.source_ranker import rank_sources
from guardrails.citation_checker import citation_checker
from guardrails.hallucination_checker import filter_supported_sources
from guardrails.unsafe_advice_blocker import is_unsafe_query
from guardrails.confidence_score import calculate_confidence
from guardrails.legal_disclaimer import legal_disclaimer
from guardrails.domain_classifier import (
    classify_legal_domain,
    out_of_domain_response,
)
from core.logger import log_error


def guardrail_agent(
    query: str,
    sources: List[Dict[str, Any]],
    llm,
    document_mode: bool = False,
    pdf_used: bool = False,
) -> Dict[str, Any]:

    try:
        safe_query = mask_pii(query)

        # =========================
        # 1. CHECK DOCUMENT CONTEXT
        # =========================
        has_document_source = any(
            str(source.get("source_type", "")).lower()
            in {"document", "pdf", "uploaded_document"}
            or bool((source.get("metadata", {}) or {}).get("document_id"))
            for source in (sources or [])
        )

        allow_document_question = bool(
            document_mode and pdf_used and has_document_source
        )

        # =========================
        # 2. DOMAIN BLOCKING
        # =========================
        # No PDF context = only legal questions allowed.
        # PDF context found = short document follow-ups allowed.
        if not allow_document_question:
            domain = classify_legal_domain(
                query=safe_query,
                llm=llm,
            )

            if domain != "LEGAL":
                response = out_of_domain_response(safe_query)
                response["blocked"] = True
                response["reason"] = "out_of_legal_domain"
                response["safe_query"] = safe_query
                response["safe_sources"] = []
                response["confidence"] = "Low"
                response["disclaimer"] = legal_disclaimer()
                response["message"] = (
                    "This question is outside Nyaya AI's legal scope. "
                    "Please ask a law-related question or a question from "
                    "the uploaded legal document."
                )
                return response

        # =========================
        # 3. UNSAFE LEGAL MISUSE
        # =========================
        if is_unsafe_query(safe_query):
            return blocked_response(safe_query)

        # =========================
        # 4. SOURCE CLEANING
        # =========================
        sanitized_sources = sanitize_sources(sources)

        if not sanitized_sources:
            return no_source_response(safe_query)

        # =========================
        # 5. RANK + VERIFY SOURCES
        # =========================
        ranked_sources = rank_sources(sanitized_sources)
        citation_checked_sources = citation_checker(ranked_sources)

        supported_sources = filter_supported_sources(
            query=safe_query,
            sources=citation_checked_sources,
        )

        # Prevent over-strict hallucination checker from deleting valid PDF context
        if not supported_sources and citation_checked_sources:
            supported_sources = citation_checked_sources[:8]

        if not supported_sources:
            return no_source_response(safe_query)

        return {
            "blocked": False,
            "safe_query": safe_query,
            "safe_sources": supported_sources,
            "confidence": calculate_confidence(supported_sources),
            "disclaimer": legal_disclaimer(),
            "message": "Guardrail validation completed.",
        }

    except Exception as error:
        log_error(
            module="guardrail_agent",
            message="Guardrail validation failed",
            error=str(error),
        )

        return {
            "blocked": False,
            "safe_query": mask_pii(query),
            "safe_sources": sanitize_sources(sources)[:8] if sources else [],
            "confidence": "Low",
            "disclaimer": legal_disclaimer(),
            "reason": "guardrail_error",
            "message": "Guardrail failed, using sanitized available context.",
        }


def sanitize_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    clean_sources = []

    for source in sources or []:
        if not source:
            continue

        metadata = source.get("metadata", {}) or {}

        if metadata.get("document_gap"):
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
        ),
    }


def no_source_response(query: str) -> Dict[str, Any]:
    return {
        "blocked": False,
        "safe_query": query,
        "safe_sources": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
        "reason": "no_verified_sources",
        "message": "No reliable verified source context was available.",
    }