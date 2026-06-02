from core.llm import get_llm
from core.config import CHEAP_MODEL, MEDIUM_MODEL, PREMIUM_MODEL
from core.logger import log_error


VALID_INTENTS = {
    "simple_legal": CHEAP_MODEL,
    "statute_lookup": CHEAP_MODEL,
    "translation": CHEAP_MODEL,
    "empty_query": CHEAP_MODEL,

    "document_question": MEDIUM_MODEL,
    "legal_research": MEDIUM_MODEL,
    "current_legal_update": MEDIUM_MODEL,
    "court_status": MEDIUM_MODEL,

    "drafting": PREMIUM_MODEL,
    "complex_lawyer_query": PREMIUM_MODEL,
}


def classify_intent_with_llm(user_query: str) -> str:
    """
    LLM-based intent classifier.
    Replaces keyword/list-based routing.
    """

    try:
        llm = get_llm(
            model=CHEAP_MODEL,
            temperature=0
        )

        prompt = f"""
You are an intent classifier for an Indian legal AI system.

Classify the user query into exactly ONE intent from this list:

simple_legal
statute_lookup
translation
empty_query
document_question
legal_research
current_legal_update
court_status
drafting
complex_lawyer_query

Rules:
- Return only the intent name.
- No explanation.
- If query is blank or meaningless, return empty_query.
- If user asks to draft notice, petition, agreement, reply, affidavit, return drafting.
- If user asks about uploaded PDF/document, return document_question.
- If user asks latest/current legal update, return current_legal_update.
- If user asks case status/court status, return court_status.
- If query needs deep case law/legal research, return legal_research.
- If user asks translation/local language conversion, return translation.
- If user asks section/article/act lookup, return statute_lookup.
- Otherwise return simple_legal.

User query:
{user_query}
"""

        response = llm.invoke(prompt)
        intent = response.content.strip().lower()

        if intent not in VALID_INTENTS:
            return "simple_legal"

        return intent

    except Exception as error:
        log_error(
            module="llm_router",
            message="Intent classification failed",
            error=str(error)
        )
        return "simple_legal"


def choose_model(intent: str) -> str:
    return VALID_INTENTS.get(intent, CHEAP_MODEL)


def run_llm(
    prompt: str,
    intent: str = None,
    user_query: str = None,
    temperature: float = 0
) -> str:
    """
    LLM-based model router.

    If intent is provided, use it.
    If intent is not provided, classify user_query/prompt using LLM.
    """

    try:
        if not intent:
            intent = classify_intent_with_llm(user_query or prompt)

        model = choose_model(intent)

        llm = get_llm(
            model=model,
            temperature=temperature
        )

        response = llm.invoke(prompt)

        return response.content

    except Exception as error:
        log_error(
            module="llm_router",
            message="LLM call failed",
            error=str(error)
        )
        raise