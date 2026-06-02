from core.llm_router import run_llm


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "hinglish": "Hindi",
    "pa": "Punjabi",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ur": "Urdu",
    "or": "Odia",
    "as": "Assamese",
    "ne": "Nepali",
    "sa": "Sanskrit",
    "kok": "Konkani",
    "mai": "Maithili",
    "doi": "Dogri",
}


def get_language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, "English")


def get_language_instruction(language_code: str) -> str:
    rules = {
        "hi": "Use Hindi in Devanagari script only.",
        "hinglish": "Use simple Hindi in Devanagari script only.",
        "pa": "Use Punjabi in Gurmukhi script only.",
        "ur": "Use Urdu in Urdu script only.",
        "bn": "Use Bengali script only.",
        "mr": "Use Marathi in Devanagari script only.",
        "gu": "Use Gujarati script only.",
        "ta": "Use Tamil script only.",
        "te": "Use Telugu script only.",
        "kn": "Use Kannada script only.",
        "ml": "Use Malayalam script only.",
        "or": "Use Odia script only.",
        "as": "Use Assamese script only.",
        "ne": "Use Nepali in Devanagari script only.",
        "sa": "Use Sanskrit in Devanagari script only.",
        "kok": "Use Konkani in Devanagari script only.",
        "mai": "Use Maithili in Devanagari script only.",
        "doi": "Use Dogri in Devanagari script only.",
    }

    if language_code == "en":
        return "Use English."

    return rules.get(
        language_code,
        "Use the same language as the user's question."
    )


def detect_explicit_response_language(text: str) -> str | None:
    if not text or not text.strip():
        return None

    prompt = f"""
You are a response-language detection agent.

Check whether the user explicitly requested the answer in a specific language.

Return exactly one language code from this list:
en
hi
hinglish
pa
bn
mr
gu
ta
te
kn
ml
ur
or
as
ne
sa
kok
mai
doi

If the user did NOT explicitly request a response language, return:
NONE

Examples:
- "answer in Hindi" -> hi
- "urdu mein batao" -> ur
- "isko tamil main likho" -> ta
- "explain in English" -> en
- "what is article 21" -> NONE

Return only the code or NONE.

User text:
{text}
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="translation",
            temperature=0
        )

        code = result.strip().lower()

        if code == "none":
            return None

        if code in LANGUAGE_NAMES:
            return code

        return None

    except Exception:
        return None


def get_translation_system_prompt(target_language: str) -> str:
    language_name = get_language_name(target_language)
    instruction = get_language_instruction(target_language)

    return f"""
You are an expert Indian legal translator.

Translate legal content into {language_name}.

Strict language rule:
{instruction}

Rules:
1. Preserve legal meaning.
2. Preserve case names.
3. Preserve party names.
4. Preserve court names.
5. Preserve citations.
6. Preserve FIR, IPC, CrPC, BNS, BNSS, Article, Section, PIL, Bail.
7. Do not add facts.
8. Do not summarize.
9. Return only translated content.
"""