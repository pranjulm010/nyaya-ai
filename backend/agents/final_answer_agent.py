from typing import List, Dict, Any

from core.llm_router import run_llm
from guardrails.legal_disclaimer import legal_disclaimer
from guardrails.confidence_score import calculate_confidence


MAX_SOURCES_FOR_CONTEXT = 8
MAX_CONTENT_PER_SOURCE = 1800


def final_answer_agent(
    query: str,
    sources: List[Dict[str, Any]],
    intent: str = "simple_legal",
    user_type: str = "public",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Production-level final answer agent.

    Responsibilities:
    1. Generate answer only from verified sources.
    2. Never call API/web/document retriever directly.
    3. Never invent laws, citations, facts, or judgments.
    4. Return structured answer with sources, confidence and disclaimer.
    """

    if not sources:
        return no_source_response()

    confidence = calculate_confidence(sources)

    formatted_sources = format_sources_for_prompt(sources)

    prompt = build_final_prompt(
        query=query,
        formatted_sources=formatted_sources,
        confidence=confidence,
        user_type=user_type,
        language=language
    )

    try:
        raw_answer = run_llm(
            prompt=prompt,
            intent=intent
        )

        if not raw_answer or not raw_answer.strip():
            return no_source_response()

        return {
            "summary": extract_summary(raw_answer),
            "answer": raw_answer,
            "sources_used": format_sources_for_response(sources),
            "confidence": confidence,
            "disclaimer": legal_disclaimer(),
            "raw_answer": raw_answer
        }

    except Exception as error:
        return {
            "summary": "Final answer generation failed.",
            "answer": (
                "I could not generate a reliable answer due to an internal error."
            ),
            "sources_used": format_sources_for_response(sources),
            "confidence": "Low",
            "disclaimer": legal_disclaimer(),
            "error": str(error),
            "raw_answer": ""
        }


def build_final_prompt(
    query: str,
    formatted_sources: str,
    confidence: str,
    user_type: str = "public",
    language: str = "en"
) -> str:

    if user_type == "lawyer":
        tone_instruction = """
Use professional legal structure.
Mention legal principles, statutory provisions, precedents,
risks, limitations, and drafting implications.
"""
    else:
        tone_instruction = """
Explain in simple language for a general Indian user.
Avoid heavy legal jargon.
"""

    return f"""
You are Nyaya AI, an Indian Legal Research Assistant.

Your answer must be based ONLY on the verified sources below.

========================
USER QUERY
========================
{query}

========================
USER TYPE
========================
{user_type}

========================
LANGUAGE
========================
{language}

========================
VERIFIED SOURCES
========================
{formatted_sources}

========================
STRICT RULES
========================
1. Use ONLY the verified sources.
2. Do NOT invent laws, judgments, cases, citations, courts, sections, or facts.
3. If sources do not support an answer, say:
   "I could not verify this from the available sources."
4. Prefer uploaded documents and official sources over blogs/news.
5. Mention source names in the answer.
6. Mention document page numbers when available.
7. Mention case citations only if present in the sources.
8. Do not provide final legal advice.
9. Do not assist in hiding evidence, forging documents, misleading court,
   evading law, or misusing legal process.
10. If sources conflict, explain the conflict and prefer stronger sources.
11. Keep the answer structured and practical.

========================
TONE
========================
{tone_instruction}

========================
OUTPUT FORMAT
========================

Summary:
[short answer]

Legal Explanation:
[clear explanation]

Important Points:
- [point 1]
- [point 2]
- [point 3]

Sources Used:
- [source name, title, page/citation/url if available]

Confidence:
{confidence}

Limitations:
[missing information or weak source issues]

Disclaimer:
{legal_disclaimer()}
"""


def format_sources_for_prompt(
    sources: List[Dict[str, Any]]
) -> str:
    if not sources:
        return "No verified sources were provided."

    formatted = ""

    for index, source in enumerate(
        sources[:MAX_SOURCES_FOR_CONTEXT],
        start=1
    ):
        formatted += f"""
SOURCE {index}

SOURCE TYPE:
{source.get("source_type", "unknown")}

SOURCE NAME:
{source.get("source_name", "unknown")}

TITLE:
{source.get("title", "Untitled")}

COURT:
{source.get("court", "")}

CITATION:
{source.get("citation", "")}

DATE:
{source.get("date", "")}

URL:
{source.get("url", "")}

DOCUMENT PAGE:
{source.get("page", "")}

TRUST SCORE:
{source.get("trust_score", "")}

RELEVANCE SCORE:
{source.get("relevance_score", "")}

CONTENT:
{truncate_text(source.get("content", ""))}

----------------------------------------
"""

    return formatted


def format_sources_for_response(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    clean_sources = []

    for source in sources[:MAX_SOURCES_FOR_CONTEXT]:
        clean_sources.append({
            "source_type": source.get("source_type"),
            "source_name": source.get("source_name"),
            "title": source.get("title"),
            "url": source.get("url"),
            "page": source.get("page"),
            "citation": source.get("citation"),
            "court": source.get("court"),
            "date": source.get("date"),
            "confidence": (
                source.get("final_score")
                or source.get("relevance_score")
                or source.get("trust_score")
            ),
        })

    return clean_sources


def truncate_text(
    text: str,
    limit: int = MAX_CONTENT_PER_SOURCE
) -> str:
    if not text:
        return ""

    text = str(text).strip()

    if len(text) <= limit:
        return text

    return text[:limit] + "... [truncated]"


def extract_summary(raw_answer: str) -> str:
    if not raw_answer:
        return ""

    lines = raw_answer.splitlines()
    capture = False
    summary_lines = []

    stop_headers = (
        "legal explanation",
        "important points",
        "sources used",
        "confidence",
        "limitations",
        "disclaimer"
    )

    for line in lines:
        stripped = line.strip()

        if stripped.lower().startswith("summary"):
            capture = True
            continue

        if capture and stripped.lower().startswith(stop_headers):
            break

        if capture and stripped:
            summary_lines.append(stripped)

    if summary_lines:
        return " ".join(summary_lines)[:500]

    return raw_answer.strip()[:500]


def no_source_response() -> Dict[str, Any]:
    return {
        "summary": "I could not verify this from the available sources.",
        "answer": (
            "I could not find reliable document, API, or web source context "
            "to answer this question safely."
        ),
        "sources_used": [],
        "confidence": "Low",
        "disclaimer": legal_disclaimer(),
        "raw_answer": (
            "I could not verify this from the available sources."
        )
    }