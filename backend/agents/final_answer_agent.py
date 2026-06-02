from typing import List, Dict, Any

from core.llm_router import run_llm
from guardrails.legal_disclaimer import legal_disclaimer
from core.logger import log_error


DOCUMENT_TYPES = {"document", "pdf", "uploaded_document"}


def final_answer_agent(
    query: str,
    sources: List[Dict[str, Any]],
    intent: str = "simple_legal",
    user_type: str = "public",
    language: str = "en",
) -> Dict[str, Any]:

    if not sources:
        return no_source_response(query)

    document_sources = get_document_sources(sources)
    external_sources = get_external_sources(sources)

    context = build_context(
        document_sources=document_sources,
        external_sources=external_sources,
    )

    has_pdf_context = bool(document_sources)

    prompt = f"""
You are Nyaya AI, an Indian legal assistant.

User question:
{query}

Intent:
{intent}

User type:
{user_type}

Target language code:
{language}

PDF/document context available:
{has_pdf_context}

Verified context:
{context}

STRICT ANSWER RULES:

1. Answer ONLY from the verified context.
2. Do not invent facts, laws, sections, judgments, dates, names, or citations.
3. If PDF/document context is present:
   - Treat PDF/document as PRIMARY source.
   - Answer from PDF first.
   - Use API/web only to support, compare, or explain.
   - Do NOT say "read the PDF" when PDF context is already provided.
4. If no PDF/document context is present:
   - Answer from API/web/legal context only.
5. If the user asks about a person, explain:
   - who the person was
   - relation with the case/legal issue
   - what happened
   - why important
6. If the answer is not available in the provided context, clearly say:
   "Available sources do not contain enough information to answer this fully."
7. Keep language simple.
8. Answer in the user's target language.
9. Include source names and page numbers if available.
10. Return only final answer text.

Recommended format:

Summary:
...

Detailed answer:
...

Key points:
- ...

Sources used:
- ...
"""

    try:
        answer = run_llm(
            prompt=prompt,
            intent=intent,
            temperature=0,
        )

    except Exception as error:
        log_error(
            module="final_answer_agent",
            message="LLM final answer failed",
            error=str(error),
        )
        return no_source_response(query)

    return {
        "summary": answer[:300],
        "answer": answer,
        "sources_used": compact_sources(sources),
        "confidence": infer_confidence(sources),
        "disclaimer": legal_disclaimer(),
        "raw_answer": answer,
    }


def get_document_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    document_sources = []

    for source in sources or []:
        source_type = str(
            source.get("source_type", "")
        ).lower().strip()

        metadata = source.get("metadata", {}) or {}

        if (
            source_type in DOCUMENT_TYPES
            or metadata.get("document_id")
            or metadata.get("document_type") in {"pdf", "docx", "txt", "md"}
        ):
            document_sources.append(source)

    return document_sources


def get_external_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    document_ids = {
        id(source)
        for source in get_document_sources(sources)
    }

    return [
        source
        for source in sources or []
        if id(source) not in document_ids
    ]


def build_context(
    document_sources: List[Dict[str, Any]],
    external_sources: List[Dict[str, Any]],
    max_document_sources: int = 10,
    max_external_sources: int = 8,
    max_chars_per_source: int = 1800,
) -> str:

    blocks = []

    if document_sources:
        blocks.append("===== PRIMARY PDF / UPLOADED DOCUMENT CONTEXT =====")

        for index, source in enumerate(
            document_sources[:max_document_sources],
            start=1,
        ):
            blocks.append(build_source_block(
                label=f"PDF SOURCE {index}",
                source=source,
                max_chars=max_chars_per_source,
            ))

    if external_sources:
        blocks.append("===== SUPPORTING API / WEBSITE CONTEXT =====")

        for index, source in enumerate(
            external_sources[:max_external_sources],
            start=1,
        ):
            blocks.append(build_source_block(
                label=f"SUPPORT SOURCE {index}",
                source=source,
                max_chars=1200,
            ))

    return "\n\n".join(blocks)


def build_source_block(
    label: str,
    source: Dict[str, Any],
    max_chars: int,
) -> str:

    return f"""
{label}
source_name: {source.get("source_name", "")}
source_type: {source.get("source_type", "")}
title: {source.get("title", "")}
court: {source.get("court", "")}
date: {source.get("date", "")}
citation: {source.get("citation", "")}
url: {source.get("url", "")}
page: {source.get("page", "")}
content:
{str(source.get("content", ""))[:max_chars]}
""".strip()


def compact_sources(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    output = []

    for source in sources[:15]:
        output.append({
            "source_name": source.get("source_name"),
            "source_type": source.get("source_type"),
            "title": source.get("title"),
            "url": source.get("url"),
            "citation": source.get("citation"),
            "court": source.get("court"),
            "date": source.get("date"),
            "page": source.get("page"),
        })

    return output


def infer_confidence(
    sources: List[Dict[str, Any]]
) -> str:

    if not sources:
        return "Low"

    has_document = bool(get_document_sources(sources))

    avg_score = sum(
        float(source.get("trust_score", 0) or 0)
        for source in sources
    ) / max(len(sources), 1)

    if has_document and avg_score >= 0.70:
        return "High"

    if avg_score >= 0.85 and len(sources) >= 2:
        return "High"

    if avg_score >= 0.65:
        return "Medium"

    return "Low"


def no_source_response(
    query: str = ""
) -> Dict[str, Any]:

    try:
        prompt = f"""
You are Nyaya AI, an Indian Legal Safety Assistant.

No verified PDF/API/web source context was found.

User query:
{query}

Rules:
1. If this is a safe legal-help question, give short lawful practical guidance.
2. If this is not law-related, say it is outside Nyaya AI's legal scope.
3. If unsafe, refuse.
4. Do not invent citations.
5. Mention emergency number 112 where relevant.
6. Return only final answer.
"""

        answer = run_llm(
            prompt=prompt,
            intent="simple_legal",
            temperature=0,
        )

    except Exception:
        answer = (
            "I could not verify this from reliable legal sources. "
            "Please ask a law-related question or consult a qualified lawyer."
        )

    return {
        "summary": answer[:300],
        "answer": answer,
        "sources_used": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
        "raw_answer": answer,
    }