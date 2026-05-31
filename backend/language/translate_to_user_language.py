from core.llm_router import run_llm
from language.regional_prompts import (
    get_translation_system_prompt,
    get_language_name
)


def translate_to_user_language(
    text: str,
    target_language: str = "en",
    preserve_citations: bool = True,
) -> str:
    """
    Translate answer back to user's language.
    """

    if not text:
        return ""

    if target_language == "en":
        return text

    language_name = get_language_name(
        target_language
    )

    system_prompt = (
        get_translation_system_prompt(
            target_language
        )
    )

    prompt = f"""
{system_prompt}

Translate this legal answer into
{language_name}.

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