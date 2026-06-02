from typing import Dict, Any, List, Optional

from agents.intent_agent import classify_intent
from agents.document_agent import document_agent
from agents.api_agent import api_agent
from agents.web_agent import web_agent
from agents.guardrail_agent import guardrail_agent
from agents.final_answer_agent import final_answer_agent
from agents.translation_agent import (
    translate_query_if_needed,
    translate_answer_if_needed,
)

from memory.memory_service import save_chat_message, get_relevant_memory
from billing.usage_tracker import can_user_continue, track_usage
from guardrails.pii_filter import mask_pii
from guardrails.legal_disclaimer import legal_disclaimer
from core.logger import log_error, log_info
from core.llm import get_llm
from core.config import CHEAP_MODEL
GENERIC_DOCUMENT_QUERIES = [
    "yeh case samjhao",
    "ye case samjhao",
    "is case ko samjhao",
    "isko samjhao",
    "explain this case",
    "summarize this case",
    "explain this document",
    "summarize this document",
    "इस केस को समझाओ",
    "यह केस समझाओ",
    "इसको समझाओ",
    "इस दस्तावेज़ को समझाओ",
    "ਇਹ ਕੇਸ ਸਮਝਾਓ",
    "ਇਹ ਕੇਸ ਦੱਸੋ",
    "இந்த கேஸை விளக்குங்கள்",
    "ఈ కేసు వివరించండి",
    "এই কেসটা বুঝাও",
    "આ કેસ સમજાવો",
]


def is_generic_document_query(query: str) -> bool:
    q = (query or "").lower().strip()
    return any(item.lower() in q for item in GENERIC_DOCUMENT_QUERIES)


def build_document_search_query(
    original_query: str,
    translated_query: str,
    document_id: Optional[str],
) -> str:
    if document_id and is_generic_document_query(original_query):
        return (
            "case facts issues arguments evidence court reasoning judgment "
            "final order conviction acquittal appellant accused prosecution "
            "defence conclusion important legal principles"
        )

    return translated_query


def has_pdf_context(document_sources: List[Dict[str, Any]]) -> bool:
    return bool(document_sources)


def build_pdf_based_search_query(
    user_query: str,
    document_sources: List[Dict[str, Any]],
) -> str:
    if not document_sources:
        return user_query

    pdf_context = " ".join(
        source.get("content", "")[:700]
        for source in document_sources[:4]
    )

    return f"""
User legal query:
{user_query}

Relevant uploaded document context:
{pdf_context}

Find related Indian legal cases, statutes, precedents, court decisions, and trusted legal commentary.
"""


def add_pdf_gap_note(
    sources: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    sources.append({
        "source_type": "system",
        "source_name": "Nyaya AI Retrieval Note",
        "title": "Uploaded document relevance note",
        "content": (
            "The uploaded document was searched first, but no sufficiently "
            "useful PDF context was retrieved for this query. The answer should "
            "therefore rely on verified API and web sources."
        ),
        "url": None,
        "page": None,
        "citation": None,
        "court": None,
        "date": None,
        "language": "en",
        "trust_score": 0.9,
        "relevance_score": 0.9,
        "metadata": {},
    })

    return sources


def router_agent(
    query: str,
    user_id: str = "anonymous",
    session_id: str = "default",
    user_type: str = "public",
    document_id: Optional[str] = None,
    document_type: Optional[str] = None,
) -> Dict[str, Any]:

    if not query or not query.strip():
        return error_response("Query is required.")

    try:
        usage_allowed = can_user_continue(
            user_id=user_id,
            user_type=user_type,
        )

        if not usage_allowed.get("allowed", True):
            return {
                "success": False,
                "blocked": True,
                "reason": "usage_limit_exceeded",
                "answer": usage_allowed.get(
                    "message",
                    "You have reached your usage limit.",
                ),
                "summary": "Usage limit exceeded.",
                "sources_used": [],
                "confidence": "Low",
                "disclaimer": legal_disclaimer(),
            }

        safe_query = mask_pii(query)

        save_chat_message(
            user_id=user_id,
            session_id=session_id,
            role="user",
            content=safe_query,
        )

        intent_data = classify_intent(
            query=safe_query,
            document_id=document_id,
        )

        intent = intent_data.get("intent", "simple_legal")

        translated_payload = translate_query_if_needed(
            query=safe_query,
            intent_data=intent_data,
        )

        search_query = translated_payload.get(
            "english_query",
            translated_payload.get("query", safe_query),
        )

        original_language = translated_payload.get(
            "original_language",
            "en",
        )

        target_language = translated_payload.get(
            "target_language",
            original_language,
        )

        document_search_query = build_document_search_query(
            original_query=safe_query,
            translated_query=search_query,
            document_id=document_id,
        )

        print("ORIGINAL QUERY:", safe_query)
        print("SEARCH QUERY:", search_query)
        print("DOCUMENT SEARCH QUERY:", document_search_query)
        print("ORIGINAL LANGUAGE:", original_language)
        print("TARGET LANGUAGE:", target_language)
        print("DOCUMENT ID:", document_id)
        print("INTENT:", intent)

        collected_sources: List[Dict[str, Any]] = []

        memory_sources = get_relevant_memory(
            query=safe_query,
            user_id=user_id,
            session_id=session_id,
            limit=3,
        )

        if memory_sources:
            collected_sources.extend(memory_sources)

        document_sources: List[Dict[str, Any]] = []

        if document_id:
            document_sources = document_agent(
                query=document_search_query,
                user_id=user_id,
                document_id=document_id,
                document_type=document_type,
                top_k=12,
            )

            print("DOCUMENT SOURCES FOUND:", len(document_sources))

        pdf_used = has_pdf_context(document_sources)

        if pdf_used:
            collected_sources.extend(document_sources)

            external_query = build_pdf_based_search_query(
                user_query=search_query,
                document_sources=document_sources,
            )

            api_sources = api_agent(
                query=external_query,
                max_results_per_source=4,
            )

            web_sources = web_agent(
                query=external_query,
                max_results_per_site=3,
            )

            print("API SOURCES FOUND:", len(api_sources))
            print("WEB SOURCES FOUND:", len(web_sources))

            collected_sources.extend(api_sources)
            collected_sources.extend(web_sources)

        else:
            if document_id:
                collected_sources = add_pdf_gap_note(collected_sources)

            api_sources = api_agent(
                query=search_query,
                max_results_per_source=5,
            )

            web_sources = web_agent(
                query=search_query,
                max_results_per_site=3,
            )

            print("API SOURCES FOUND:", len(api_sources))
            print("WEB SOURCES FOUND:", len(web_sources))

            collected_sources.extend(api_sources)
            collected_sources.extend(web_sources)

        if not collected_sources:
            collected_sources.extend(
                api_agent(
                    query=search_query,
                    max_results_per_source=3,
                )
            )
        guardrail_llm = get_llm(
            model=CHEAP_MODEL,
            temperature=0
        )

        guardrail_payload = guardrail_agent(
        query=search_query,
        sources=collected_sources,
        llm=guardrail_llm
        )
        

        if guardrail_payload.get("blocked"):
            blocked_answer = guardrail_payload.get(
                "message",
                "This request cannot be processed safely.",
            )

            blocked_payload = {
                "answer": blocked_answer,
                "sources_used": [],
                "confidence": "Low",
                "disclaimer": guardrail_payload.get(
                    "disclaimer",
                    legal_disclaimer(),
                ),
            }

            blocked_payload = translate_answer_if_needed(
                answer_payload=blocked_payload,
                target_language=target_language,
            )

            save_chat_message(
                user_id=user_id,
                session_id=session_id,
                role="assistant",
                content=blocked_payload.get("answer", ""),
            )

            return {
                "success": True,
                "blocked": True,
                "intent": intent,
                "intent_reason": intent_data.get("reason"),
                "language": target_language,
                "original_language": original_language,
                "translated": translated_payload.get("translated", False),
                "pdf_used": False,
                "summary": "Request blocked for safety.",
                "answer": blocked_payload.get("answer"),
                "sources_used": [],
                "confidence": "Low",
                "disclaimer": blocked_payload.get(
                    "disclaimer",
                    legal_disclaimer(),
                ),
            }

        final_payload = final_answer_agent(
            query=guardrail_payload.get("safe_query", search_query),
            sources=guardrail_payload.get("safe_sources", []),
            intent=intent,
            user_type=user_type,
            language=target_language,
        )

        final_payload = translate_answer_if_needed(
            answer_payload=final_payload,
            target_language=target_language,
        )

        track_usage(
            user_id=user_id,
            user_type=user_type,
            intent=intent,
            sources_count=len(collected_sources),
        )

        save_chat_message(
            user_id=user_id,
            session_id=session_id,
            role="assistant",
            content=final_payload.get("answer", ""),
        )

        log_info(
            module="router_agent",
            message=(
                f"Query completed for user={user_id}, "
                f"intent={intent}, pdf_used={pdf_used}, "
                f"language={target_language}"
            ),
        )

        return {
            "success": True,
            "blocked": False,
            "intent": intent,
            "intent_reason": intent_data.get("reason"),
            "language": target_language,
            "original_language": original_language,
            "translated": translated_payload.get("translated", False),
            "pdf_used": pdf_used,
            "summary": final_payload.get("summary"),
            "answer": final_payload.get("answer"),
            "sources_used": final_payload.get("sources_used", []),
            "confidence": final_payload.get("confidence"),
            "disclaimer": final_payload.get(
                "disclaimer",
                legal_disclaimer(),
            ),
        }

    except Exception as error:
        log_error(
            module="router_agent",
            message="Router failed",
            error=str(error),
        )

        return error_response(
            "Something went wrong while processing your legal query."
        )


def error_response(message: str) -> Dict[str, Any]:
    return {
        "success": False,
        "blocked": False,
        "intent": None,
        "summary": message,
        "answer": message,
        "sources_used": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
    }