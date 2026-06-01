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


EXPLICIT_LANGUAGE_KEYWORDS = {
    "en": ["answer in english", "reply in english", "respond in english", "english mein", "english me"],
    "hi": ["answer in hindi", "reply in hindi", "respond in hindi", "hindi mein", "hindi me"],
    "ur": ["answer in urdu", "reply in urdu", "respond in urdu", "urdu mein", "urdu me"],
    "pa": ["answer in punjabi", "reply in punjabi", "respond in punjabi", "punjabi mein", "punjabi me"],
    "ta": ["answer in tamil", "reply in tamil", "respond in tamil", "tamil mein", "tamil me"],
    "te": ["answer in telugu", "reply in telugu", "respond in telugu", "telugu mein", "telugu me"],
    "bn": ["answer in bengali", "reply in bengali", "respond in bengali", "bengali mein", "bengali me"],
    "mr": ["answer in marathi", "reply in marathi", "respond in marathi", "marathi mein", "marathi me"],
    "gu": ["answer in gujarati", "reply in gujarati", "respond in gujarati", "gujarati mein", "gujarati me"],
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

    return rules.get(language_code, "Use the same language as the user's question.")


def detect_explicit_response_language(text: str) -> str | None:
    if not text:
        return None

    lower_text = text.lower()

    for language_code, keywords in EXPLICIT_LANGUAGE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower_text:
                return language_code

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