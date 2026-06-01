from core.llm_router import run_llm
from language.regional_prompts import get_language_name


def translate_to_english(
    text: str,
    source_language: str = "auto",
    preserve_legal_terms: bool = True,
) -> str:

    if not text or not text.strip():
        return ""

    if source_language == "en":
        return text

    language_name = get_language_name(source_language)

    prompt = f"""
You are a legal query translation agent.

Translate this Indian legal query into English.

Source language:
{language_name}

Rules:
1. Preserve legal meaning.
2. Preserve case names.
3. Preserve person names.
4. Preserve party names.
5. Preserve court names.
6. Preserve legal words:
   FIR, Bail, PIL, Article, Section, IPC, CrPC, BNS, BNSS,
   High Court, Supreme Court.
7. Do not answer the query.
8. Do not add facts.
9. Return only English translation.

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
        print("TRANSLATE TO ENGLISH ERROR:", error)
        return text