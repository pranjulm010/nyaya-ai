LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "mr": "Marathi",
    "ur": "Urdu",
}


def get_language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(
        code,
        "English"
    )


def get_translation_system_prompt(
    target_language: str
) -> str:

    language_name = get_language_name(
        target_language
    )

    return f"""
You are an expert Indian legal translator.

Translate legal content into {language_name}.

Rules:
1. Preserve legal meaning.
2. Do not change case names.
3. Do not modify citations.
4. Preserve FIR, IPC, CrPC, BNS, BNSS,
   Article, Section, PIL, Bail.
5. Keep legal terminology accurate.
6. Keep headings and formatting same.
7. Do not summarize.
8. Return only translated content.
"""