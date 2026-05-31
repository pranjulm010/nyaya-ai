from core.llm_router import run_llm


def translate_to_english(
    text: str,
    source_language: str = "auto",
    preserve_legal_terms: bool = True,
) -> str:
    """
    Translate Indian regional language
    to English for retrieval/search.
    """

    if not text:
        return ""

    prompt = f"""
Translate this legal query into English.

Rules:
1. Preserve legal words:
FIR, Bail, PIL, Article,
Section, IPC, CrPC, BNS,
BNSS, High Court,
Supreme Court.

2. Do not answer query.
3. Do not add facts.
4. Return only translation.

Source language:
{source_language}

Text:
{text}
"""

    try:
        translated = run_llm(
            prompt=prompt,
            intent="translation"
        )

        return translated.strip()

    except Exception:
        return text