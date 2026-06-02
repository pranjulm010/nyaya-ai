from typing import Dict, Any, Optional
import json
import re

from core.llm_router import run_llm

VALID_INTENTS = {
    "empty_query", "simple_legal", "statute_lookup", "document_question",
    "legal_research", "current_legal_update", "court_status", "drafting",
    "complex_lawyer_query", "translation",
}


def detect_intent(query: str, document_id: Optional[str] = None) -> str:
    return classify_intent(query=query, document_id=document_id)["intent"]


def classify_intent(query: str, document_id: Optional[str] = None) -> Dict[str, Any]:
    if not query or not query.strip():
        return build_result("empty_query", reason="Query is empty.")

    if document_id:
        return build_result(
            intent="document_question",
            needs_document=True,
            needs_api=True,
            needs_web=True,
            needs_translation=True,
            needs_premium_model=False,
            reason="Uploaded document is active; route PDF/document context first, then API + websites + LLM.",
        )

    prompt = f"""
You are the LLM intent classifier for Nyaya AI, an Indian legal AI system.
Classify the user query by meaning, not by keyword matching.

User query:
{query}

Return ONLY valid JSON:
{{
  "intent": "empty_query | simple_legal | statute_lookup | document_question | legal_research | current_legal_update | court_status | drafting | complex_lawyer_query | translation",
  "needs_document": false,
  "needs_api": true,
  "needs_web": true,
  "needs_translation": true,
  "needs_premium_model": false,
  "reason": "short reason"
}}

Routing rules:
- Without uploaded PDF/document: use LLM + API + websites for legal questions.
- With uploaded PDF/document: document_question is forced before this prompt is used.
- Drafting legal notice, complaint, petition, agreement, affidavit, reply = drafting.
- Case status, CNR, next hearing date = court_status.
- Judgments, precedents, landmark cases = legal_research.
- Section, article, act, bare act, provision = statute_lookup.
- Latest/recent/current legal development = current_legal_update.
- Translation/rewrite into a language = translation.
- Complex multi-issue lawyer-style analysis = complex_lawyer_query.
- Ordinary lawful legal help = simple_legal.
- Indian language/Hinglish should set needs_translation true.
"""
    try:
        raw = run_llm(prompt=prompt, intent="simple_legal", temperature=0)
        data = parse_json_safely(raw)
        intent = data.get("intent", "simple_legal")
        if intent not in VALID_INTENTS:
            intent = "simple_legal"
        return build_result(
            intent=intent,
            needs_document=bool(data.get("needs_document", False)),
            needs_api=bool(data.get("needs_api", True)),
            needs_web=bool(data.get("needs_web", True)),
            needs_translation=bool(data.get("needs_translation", True)),
            needs_premium_model=bool(data.get("needs_premium_model", intent in {"complex_lawyer_query", "drafting"})),
            reason=data.get("reason", "LLM-based intent classification."),
        )
    except Exception:
        return build_result("simple_legal", needs_api=True, needs_web=True, needs_translation=True, reason="Fallback after LLM classification failed.")


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


def build_result(intent: str, needs_document: bool = False, needs_api: bool = True, needs_web: bool = True, needs_translation: bool = True, needs_premium_model: bool = False, reason: str = "") -> Dict[str, Any]:
    return {
        "intent": intent,
        "needs_document": needs_document,
        "needs_api": needs_api,
        "needs_web": needs_web,
        "needs_translation": needs_translation,
        "needs_premium_model": needs_premium_model,
        "reason": reason,
    }
