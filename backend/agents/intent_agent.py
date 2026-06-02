from typing import Dict, Any, Optional
import json
import re

from core.llm_router import run_llm


VALID_INTENTS = {
    "empty_query",
    "simple_legal",
    "statute_lookup",
    "document_question",
    "legal_research",
    "current_legal_update",
    "court_status",
    "drafting",
    "complex_lawyer_query",
    "translation",
}


def detect_intent(
    query: str,
    document_id: Optional[str] = None
) -> str:
    result = classify_intent(
        query=query,
        document_id=document_id
    )
    return result["intent"]


def classify_intent(
    query: str,
    document_id: Optional[str] = None
) -> Dict[str, Any]:

    if not query or not query.strip():
        return build_result(
            intent="empty_query",
            reason="Query is empty."
        )

    if document_id:
        return build_result(
            intent="document_question",
            needs_document=True,
            needs_api=True,
            needs_web=True,
            needs_translation=True,
            reason="Uploaded document is active, so document + API + web should be used."
        )

    prompt = f"""
You are an intent classifier for Nyaya AI, an Indian Legal AI system.

Classify the user query into exactly ONE intent:

empty_query
simple_legal
statute_lookup
document_question
legal_research
current_legal_update
court_status
drafting
complex_lawyer_query
translation

Return ONLY valid JSON in this exact format:

{{
  "intent": "...",
  "needs_document": true,
  "needs_api": true,
  "needs_web": false,
  "needs_translation": false,
  "needs_premium_model": false,
  "reason": "short reason"
}}

Rules:
- Draft notice/petition/agreement/affidavit/complaint/reply = drafting.
- Uploaded PDF/document/case file = document_question.
- Latest/current/recent legal update = current_legal_update.
- Case status/CNR/hearing date/next date = court_status.
- Judgments/case law/precedents = legal_research.
- Section/article/act/statute = statute_lookup.
- Translation/language conversion = translation.
- Indian language or Hinglish = needs_translation true.
- Normal legal query = simple_legal.

User query:
{query}
"""

    try:
        raw = run_llm(
            prompt=prompt,
            intent="simple_legal",
            temperature=0
        )

        data = parse_json_safely(raw)

        intent = data.get("intent", "simple_legal")

        if intent not in VALID_INTENTS:
            intent = "simple_legal"

        return build_result(
            intent=intent,
            needs_document=bool(data.get("needs_document", False)),
            needs_api=bool(data.get("needs_api", True)),
            needs_web=bool(data.get("needs_web", False)),
            needs_translation=bool(data.get("needs_translation", False)),
            needs_premium_model=bool(data.get("needs_premium_model", False)),
            reason=data.get("reason", "LLM-based intent classification.")
        )

    except Exception:
        return build_result(
            intent="simple_legal",
            needs_api=True,
            needs_translation=True,
            reason="Fallback intent because LLM classification failed."
        )


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


def build_result(
    intent: str,
    needs_document: bool = False,
    needs_api: bool = False,
    needs_web: bool = False,
    needs_translation: bool = False,
    needs_premium_model: bool = False,
    reason: str = ""
) -> Dict[str, Any]:

    return {
        "intent": intent,
        "needs_document": needs_document,
        "needs_api": needs_api,
        "needs_web": needs_web,
        "needs_translation": needs_translation,
        "needs_premium_model": needs_premium_model,
        "reason": reason,
    }