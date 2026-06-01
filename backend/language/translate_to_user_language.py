from core.llm_router import run_llm
from language.regional_prompts import (
    get_translation_system_prompt,
    get_language_name,
    get_language_instruction,
)


def translate_to_user_language(
    text: str,
    target_language: str = "en",
    preserve_citations: bool = True,
) -> str:

    if not text or not text.strip():
        return ""

    if target_language == "en":
        return text

    language_name = get_language_name(target_language)
    system_prompt = get_translation_system_prompt(target_language)
    language_instruction = get_language_instruction(target_language)

    prompt = f"""
{system_prompt}

VERY IMPORTANT:
The final answer must be in {language_name}.
{language_instruction}
Do not return English unless the user explicitly asked for English.

Translate this legal answer into {language_name}.

Rules:
1. Keep the answer in the user's required language.
2. Preserve case names.
3. Preserve person names.
4. Preserve party names.
5. Preserve court names.
6. Preserve citations.
7. Preserve source names like Indian Kanoon, Supreme Court, LiveLaw.
8. Preserve Section, Article, IPC, CrPC, BNS, BNSS, FIR, PIL, Bail.
9. Do not add new facts.
10. Do not remove disclaimer.
11. Do not summarize unless the original answer is summary.
12. Return only translated answer.

Text:
{text}
"""

    try:
        translated = run_llm(
            prompt=prompt,
            intent="translation",
        )

        return translated.strip()

    except Exception as error:
        print("TRANSLATE TO USER LANGUAGE ERROR:", error)
        return text