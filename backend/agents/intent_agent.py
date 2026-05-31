from typing import Dict, Any, Optional


LEGAL_RESEARCH_KEYWORDS = [
    "case", "judgment", "judgement", "citation", "precedent",
    "supreme court", "high court", "court", "order",
    "bail", "writ", "petition", "appeal", "fir",
    "legal principle", "ratio", "held",
]

STATUTE_KEYWORDS = [
    "section", "article", "act", "law", "ipc", "crpc",
    "bns", "bnss", "constitution", "provision", "rule",
    "bare act", "sub section", "clause",
]

DRAFTING_KEYWORDS = [
    "draft", "create", "write", "prepare", "format",
    "notice", "petition", "agreement", "affidavit",
    "legal notice", "reply", "application", "contract",
    "complaint", "plaint", "written statement",
]

DOCUMENT_KEYWORDS = [
    "document", "uploaded", "file", "pdf", "docx", "txt",
    "agreement", "contract", "clause", "page",
    "analyze this", "summarize this", "review this",
    "this case", "this document", "this pdf",
    "explain this", "isko samjhao", "yeh case", "ye case",
    "is case", "case samjhao", "hindi main samjhao",
    "hindi mein samjhao", "इस केस", "यह केस", "समझाओ",
]

CURRENT_KEYWORDS = [
    "latest", "recent", "today", "current", "new",
    "update", "news", "2025", "2026",
]

COURT_STATUS_KEYWORDS = [
    "case status", "cnr", "hearing date", "next date",
    "court status", "case number", "filing number",
]

TRANSLATION_KEYWORDS = [
    "translate", "hindi", "english", "hinglish",
    "tamil", "telugu", "bengali", "marathi",
    "gujarati", "kannada", "malayalam", "punjabi", "urdu",
]


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

    q = (query or "").lower().strip()

    if not q:
        return build_result(
            intent="empty_query",
            reason="Query is empty."
        )

    needs_translation = (
        has_any(q, TRANSLATION_KEYWORDS)
        or contains_indic_text(q)
        or has_hinglish_words(q)
    )

    # MOST IMPORTANT FIX:
    # If frontend sends document_id, always search uploaded document.
    if document_id:
        return build_result(
            intent="document_question",
            needs_document=True,
            needs_api=False,
            needs_web=False,
            needs_translation=needs_translation,
            reason="Uploaded document is active, so query should use document context."
        )

    if has_any(q, COURT_STATUS_KEYWORDS):
        return build_result(
            intent="court_status",
            needs_api=True,
            needs_web=True,
            needs_translation=needs_translation,
            reason="Query asks about court status or case tracking."
        )

    if has_any(q, DRAFTING_KEYWORDS):
        return build_result(
            intent="drafting",
            needs_document=True,
            needs_api=True,
            needs_web=False,
            needs_translation=needs_translation,
            needs_premium_model=True,
            reason="Query asks for legal drafting."
        )

    if has_any(q, DOCUMENT_KEYWORDS):
        return build_result(
            intent="document_question",
            needs_document=True,
            needs_api=False,
            needs_web=False,
            needs_translation=needs_translation,
            reason="Query refers to uploaded document analysis."
        )

    if has_any(q, CURRENT_KEYWORDS):
        return build_result(
            intent="current_legal_update",
            needs_api=True,
            needs_web=True,
            needs_translation=needs_translation,
            reason="Query asks for latest/current legal information."
        )

    if has_any(q, LEGAL_RESEARCH_KEYWORDS):
        return build_result(
            intent="legal_research",
            needs_api=True,
            needs_web=True,
            needs_translation=needs_translation,
            reason="Query asks for cases, judgments, courts or precedents."
        )

    if has_any(q, STATUTE_KEYWORDS):
        return build_result(
            intent="statute_lookup",
            needs_api=True,
            needs_web=False,
            needs_translation=needs_translation,
            reason="Query asks about statute, section, act or article."
        )

    return build_result(
        intent="simple_legal",
        needs_api=True,
        needs_translation=needs_translation,
        reason="General legal information query."
    )


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


def has_any(text: str, keywords: list) -> bool:
    return any(keyword in text for keyword in keywords)


def has_hinglish_words(text: str) -> bool:
    hinglish_words = [
        "samjhao", "samjhaao", "batao", "bataiye",
        "kya", "kaise", "kyu", "mein", "main",
        "hindi", "case samjhao", "yeh", "ye",
    ]

    return any(word in text for word in hinglish_words)


def contains_indic_text(text: str) -> bool:
    for char in text:
        code = ord(char)

        if (
            0x0900 <= code <= 0x097F or
            0x0980 <= code <= 0x09FF or
            0x0A00 <= code <= 0x0A7F or
            0x0A80 <= code <= 0x0AFF or
            0x0B80 <= code <= 0x0BFF or
            0x0C00 <= code <= 0x0C7F or
            0x0C80 <= code <= 0x0CFF or
            0x0D00 <= code <= 0x0D7F or
            0x0600 <= code <= 0x06FF
        ):
            return True

    return False