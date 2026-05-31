from langchain_groq import ChatGroq

from core.config import (
    GROQ_API_KEY,
    DEFAULT_TEMPERATURE,
)


def get_llm(
    model: str,
    temperature: float = DEFAULT_TEMPERATURE
):
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in .env file."
        )

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=model,
        temperature=temperature,
    )