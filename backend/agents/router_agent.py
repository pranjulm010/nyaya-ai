from typing import Dict, Any, List, Optional
import json
import re

from agents.intent_agent import classify_intent
from agents.document_agent import document_agent
from agents.api_agent import api_agent
from agents.web_agent import web_agent
from agents.guardrail_agent import guardrail_agent
from agents.final_answer_agent import final_answer_agent, no_source_response
from agents.translation_agent import translate_query_if_needed, translate_answer_if_needed
from memory.memory_service import save_chat_message, get_relevant_memory
from billing.usage_tracker import can_user_continue, track_usage
from guardrails.pii_filter import mask_pii
from guardrails.legal_disclaimer import legal_disclaimer
from core.logger import log_error, log_info
from core.llm import get_llm
from core.llm_router import run_llm
from core.config import CHEAP_MODEL


GENERIC_DOCUMENT_QUERY_PATTERNS = [
    "yeh case samjhao", "ye case samjhao", "is case ko samjhao", "isko samjhao",
    "explain this case", "summarize this case", "explain this document", "summarize this document",
    "what happened", "what is this", "explain it", "summarize it", "tell me about this",
    "इस केस को समझाओ", "यह केस समझाओ", "इसको समझाओ", "इस दस्तावेज़ को समझाओ",
    "ਕੀ ਹੋਇਆ", "ਇਹ ਕੇਸ ਸਮਝਾਓ", "இந்த கேஸை விளக்குங்கள்", "ఈ కేసు వివరించండి",
]


def router_agent(
    query: str,
    user_id: str = "anonymous",
    session_id: str = "default",
    user_type: str = "public",
    document_id: Optional[str] = None,
    document_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Correct orchestration:

    1. If a PDF/document is uploaded:
       - Try uploaded document first.
       - Use API + websites only to support/verify document context.
       - Allow short contextual follow-ups ONLY when relevant PDF context is found.
       - If the question is unrelated to PDF and not legal, block it.

    2. If no PDF/document is uploaded:
       - No document retrieval.
       - Use API + websites + LLM only for legal-domain queries.
       - Non-legal queries like "what is python" are blocked by guardrail.

    3. No keyword-based source selection:
       - API and web agents select connectors using LLM.
    """

    if not query or not query.strip():
        return error_response("Query is required.")

    try:
        usage_allowed = can_user_continue(user_id=user_id, user_type=user_type)
        if not usage_allowed.get("allowed", True):
            return {
                "success": False,
                "blocked": True,
                "reason": "usage_limit_exceeded",
                "answer": usage_allowed.get("message", "You have reached your usage limit."),
                "summary": "Usage limit exceeded.",
                "sources_used": [],
                "confidence": "Low",
                "disclaimer": legal_disclaimer(),
            }

        safe_query = mask_pii(query)
        save_chat_message(user_id=user_id, session_id=session_id, role="user", content=safe_query)

        document_mode = bool(document_id)

        if document_mode:
            intent_data = {
                "intent": "document_question",
                "needs_document": True,
                "needs_api": True,
                "needs_web": True,
                "needs_translation": True,
                "needs_premium_model": False,
                "reason": "Uploaded document is active; document retrieval is attempted first.",
            }
        else:
            intent_data = classify_intent(query=safe_query, document_id=None)

        intent = intent_data.get("intent", "simple_legal")

        translated_payload = translate_query_if_needed(query=safe_query, intent_data=intent_data)
        search_query = translated_payload.get("english_query") or translated_payload.get("query") or safe_query
        original_language = translated_payload.get("original_language", "en")
        target_language = translated_payload.get("target_language", original_language)

        print("ORIGINAL QUERY:", safe_query)
        print("SEARCH QUERY:", search_query)
        print("ORIGINAL LANGUAGE:", original_language)
        print("TARGET LANGUAGE:", target_language)
        print("DOCUMENT ID:", document_id)
        print("DOCUMENT MODE:", document_mode)
        print("INTENT:", intent)

        collected_sources: List[Dict[str, Any]] = []

        memory_sources = get_relevant_memory(query=safe_query, user_id=user_id, session_id=session_id, limit=3)
        if memory_sources:
            collected_sources.extend(memory_sources)

        document_sources: List[Dict[str, Any]] = []
        pdf_used = False

        if document_mode:
            document_search_query = build_document_search_query(
                original_query=safe_query,
                translated_query=search_query,
            )
            print("DOCUMENT SEARCH QUERY:", document_search_query)

            raw_document_sources = document_agent(
                query=document_search_query,
                user_id=user_id,
                document_id=document_id,
                document_type=document_type,
                top_k=12,
            )
            print("RAW DOCUMENT SOURCES FOUND:", len(raw_document_sources))

            document_sources = keep_only_relevant_document_sources(
                user_query=search_query,
                original_query=safe_query,
                sources=mark_document_sources(raw_document_sources, document_id),
            )
            print("RELEVANT DOCUMENT SOURCES FOUND:", len(document_sources))

            pdf_used = bool(document_sources)

        if pdf_used:
            # Uploaded PDF is PRIMARY truth source.
            collected_sources.extend(document_sources)
            external_query = build_pdf_based_external_query(search_query, document_sources)
            collected_sources.extend(collect_external_sources(external_query, pdf_used=True))
        else:
            # Important: if document exists but retrieval found no relevant PDF context,
            # do NOT automatically allow unrelated questions. Guardrail will block non-legal.
            if document_mode:
                collected_sources = add_pdf_gap_note(collected_sources)

            collected_sources.extend(collect_external_sources(search_query, pdf_used=False))

        guardrail_llm = get_llm(model=CHEAP_MODEL, temperature=0)
        guardrail_payload = guardrail_agent(
            query=search_query,
            sources=collected_sources,
            llm=guardrail_llm,
            document_mode=document_mode,
            pdf_used=pdf_used,
        )

        if guardrail_payload.get("blocked"):
            return build_blocked_response(
                guardrail_payload=guardrail_payload,
                intent=intent,
                intent_data=intent_data,
                target_language=target_language,
                original_language=original_language,
                translated_payload=translated_payload,
                user_id=user_id,
                session_id=session_id,
                pdf_used=pdf_used,
            )

        safe_sources = guardrail_payload.get("safe_sources", [])
        if not safe_sources:
            final_payload = no_source_response(search_query)
        else:
            final_payload = final_answer_agent(
                query=guardrail_payload.get("safe_query", search_query),
                sources=safe_sources,
                intent=intent,
                user_type=user_type,
                language=target_language,
            )

        final_payload = translate_answer_if_needed(answer_payload=final_payload, target_language=target_language)

        track_usage(user_id=user_id, user_type=user_type, intent=intent, sources_count=len(collected_sources))
        save_chat_message(user_id=user_id, session_id=session_id, role="assistant", content=final_payload.get("answer", ""))

        log_info(
            "router_agent",
            f"Query completed user={user_id}, intent={intent}, pdf_used={pdf_used}, language={target_language}",
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
            "disclaimer": final_payload.get("disclaimer", legal_disclaimer()),
        }

    except Exception as error:
        log_error("router_agent", "Router failed", str(error))
        return error_response("Something went wrong while processing your legal query.")


def is_generic_document_query(query: str) -> bool:
    q = (query or "").lower().strip()
    return any(pattern.lower() in q for pattern in GENERIC_DOCUMENT_QUERY_PATTERNS)


def build_document_search_query(original_query: str, translated_query: str) -> str:
    """
    LLM/RAG-friendly query expansion for every PDF question.
    Keeps exact user terms and expands legal-document semantics.
    """
    if is_generic_document_query(original_query) or is_generic_document_query(translated_query):
        return f"""
Uploaded legal document is active.
The user is asking a broad follow-up about the uploaded document.
Original user query: {original_query}
English query: {translated_query}

Retrieve the most relevant chunks covering:
case facts, parties, persons, timeline, allegations, evidence, witness statements,
arguments, legal issues, court reasoning, cited provisions, cited cases, judgment,
final order, and important conclusions.
"""

    return f"""
Uploaded legal document is active.
Answer this specific user question from the uploaded document first.
Original user query: {original_query}
English query: {translated_query}

Retrieve chunks mentioning exact entities/terms in the query and nearby context:
person identity, role in case, relationship with parties, facts, evidence,
statements, court findings, reasoning, and final conclusion.
"""


def mark_document_sources(sources: List[Dict[str, Any]], document_id: Optional[str]) -> List[Dict[str, Any]]:
    marked = []
    for source in sources or []:
        item = dict(source)
        item["source_type"] = "document"
        item["source_name"] = item.get("source_name") or "Uploaded document"
        metadata = dict(item.get("metadata", {}) or {})
        if document_id:
            metadata["document_id"] = document_id
        item["metadata"] = metadata
        item["trust_score"] = max(float(item.get("trust_score", 0) or 0), 0.98)
        item["relevance_score"] = max(float(item.get("relevance_score", 0) or 0), 0.90)
        marked.append(item)
    return marked


def keep_only_relevant_document_sources(
    user_query: str,
    original_query: str,
    sources: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Prevents unrelated PDF chunks from making non-legal questions pass.
    Example: with a PDF uploaded, "what is python" should not be answered unless
    the PDF actually contains relevant Python context.
    """
    if not sources:
        return []

    # Generic document questions are intentionally about the active document.
    if is_generic_document_query(user_query) or is_generic_document_query(original_query):
        return sources[:10]

    context = "\n\n".join(
        f"SOURCE {i+1}: {str(source.get('content', ''))[:900]}"
        for i, source in enumerate(sources[:8])
    )

    prompt = f"""
You are a strict relevance judge for an uploaded Indian legal document.

User question:
{user_query}

Original question:
{original_query}

Retrieved document chunks:
{context}

Decide whether these chunks actually answer or directly relate to the user's question.
Do NOT mark relevant just because a PDF exists.
For legal case follow-ups about a person, fact, role, incident, court reasoning, evidence, timeline, judgment or case summary, mark relevant if the chunks discuss it.
For unrelated general knowledge questions like "what is python", mark not relevant unless the chunks actually discuss that topic.

Return ONLY JSON:
{{"relevant": true, "keep_indexes": [1,2,3], "reason": "short"}}
"""
    try:
        raw = run_llm(prompt=prompt, intent="document_question", temperature=0)
        data = parse_json_safely(raw)
        if not bool(data.get("relevant", False)):
            return []
        keep_indexes = data.get("keep_indexes") or []
        kept = []
        for idx in keep_indexes:
            try:
                int_idx = int(idx) - 1
                if 0 <= int_idx < len(sources[:8]):
                    kept.append(sources[int_idx])
            except Exception:
                continue
        return kept or sources[:5]
    except Exception as error:
        log_error("router_agent", "Document relevance check failed", str(error))
        # Safe fallback: keep only top few. Guardrail still performs domain check if pdf_used becomes true.
        return sources[:5]


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


def build_pdf_based_external_query(user_query: str, document_sources: List[Dict[str, Any]]) -> str:
    pdf_context = "\n".join(str(source.get("content", ""))[:900] for source in document_sources[:5])
    return f"""
User legal/document query:
{user_query}

Uploaded PDF/document context extracted first:
{pdf_context}

Task for API/web search:
Find Indian statutes, case law, official court sources, citations, or trusted legal commentary that verify, explain, supplement, or contrast with this uploaded document context.
"""


def collect_external_sources(search_query: str, pdf_used: bool) -> List[Dict[str, Any]]:
    api_sources = api_agent(query=search_query, max_results_per_source=4 if pdf_used else 5)
    web_sources = web_agent(query=search_query, max_results_per_site=3)
    print("API SOURCES FOUND:", len(api_sources))
    print("WEB SOURCES FOUND:", len(web_sources))
    return api_sources + web_sources


def add_pdf_gap_note(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sources.append({
        "source_type": "system",
        "source_name": "Nyaya AI Retrieval Note",
        "title": "Uploaded document retrieval note",
        "content": (
            "An uploaded document is active, so document retrieval was attempted first, "
            "but no sufficiently relevant document chunks were found for this query. "
            "If the query is not legal-domain, it must be blocked instead of answered from general web/LLM."
        ),
        "url": None,
        "page": None,
        "citation": None,
        "court": None,
        "date": None,
        "language": "en",
        "trust_score": 0.50,
        "relevance_score": 0.50,
        "metadata": {"document_gap": True},
    })
    return sources


def build_blocked_response(
    guardrail_payload: Dict[str, Any],
    intent: str,
    intent_data: Dict[str, Any],
    target_language: str,
    original_language: str,
    translated_payload: Dict[str, Any],
    user_id: str,
    session_id: str,
    pdf_used: bool = False,
) -> Dict[str, Any]:
    blocked_payload = {
        "answer": guardrail_payload.get("message", "This request cannot be processed safely."),
        "sources_used": [],
        "confidence": "Low",
        "disclaimer": guardrail_payload.get("disclaimer", legal_disclaimer()),
    }
    blocked_payload = translate_answer_if_needed(answer_payload=blocked_payload, target_language=target_language)
    save_chat_message(user_id=user_id, session_id=session_id, role="assistant", content=blocked_payload.get("answer", ""))
    return {
        "success": True,
        "blocked": True,
        "intent": intent,
        "intent_reason": intent_data.get("reason"),
        "language": target_language,
        "original_language": original_language,
        "translated": translated_payload.get("translated", False),
        "pdf_used": pdf_used,
        "summary": "Request blocked by legal-domain/safety guardrail.",
        "answer": blocked_payload.get("answer"),
        "sources_used": [],
        "confidence": "Low",
        "disclaimer": blocked_payload.get("disclaimer", legal_disclaimer()),
    }


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
