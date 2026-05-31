from core.llm import get_llm
from core.config import (
    CHEAP_MODEL,
    MEDIUM_MODEL,
    PREMIUM_MODEL,
)
from core.logger import log_error


CHEAP_INTENTS = [
    "simple_legal",
    "statute_lookup",
    "translation",
    "empty_query",
]

MEDIUM_INTENTS = [
    "document_question",
    "legal_research",
    "current_legal_update",
    "court_status",
]

PREMIUM_INTENTS = [
    "drafting",
    "complex_lawyer_query",
]


def choose_model(intent: str = "simple_legal") -> str:
    if intent in CHEAP_INTENTS:
        return CHEAP_MODEL

    if intent in MEDIUM_INTENTS:
        return MEDIUM_MODEL

    if intent in PREMIUM_INTENTS:
        return PREMIUM_MODEL

    return CHEAP_MODEL


def run_llm(
    prompt: str,
    intent: str = "simple_legal",
    temperature: float = 0
) -> str:
    """
    Low-cost model router.

    Simple query -> cheap model
    Legal research/doc query -> medium model
    Drafting/lawyer query -> premium model
    """

    try:
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