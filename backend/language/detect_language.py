from core.llm_router import run_llm


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "hinglish": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
    "or": "Odia",
    "as": "Assamese",
    "ne": "Nepali",
    "sa": "Sanskrit",
    "kok": "Konkani",
    "mai": "Maithili",
    "doi": "Dogri",
}


def fallback_script_detection(text: str) -> str:
    for char in text:
        code = ord(char)

        if 0x0600 <= code <= 0x06FF:
            return "ur"
        if 0x0900 <= code <= 0x097F:
            return "hi"
        if 0x0980 <= code <= 0x09FF:
            return "bn"
        if 0x0A00 <= code <= 0x0A7F:
            return "pa"
        if 0x0A80 <= code <= 0x0AFF:
            return "gu"
        if 0x0B00 <= code <= 0x0B7F:
            return "or"
        if 0x0B80 <= code <= 0x0BFF:
            return "ta"
        if 0x0C00 <= code <= 0x0C7F:
            return "te"
        if 0x0C80 <= code <= 0x0CFF:
            return "kn"
        if 0x0D00 <= code <= 0x0D7F:
            return "ml"

    return "en"


def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"

    prompt = f"""
You are a language detection agent for an Indian legal AI.

Detect the language of the user's text.

Return exactly one code from this list:
en
hi
hinglish
ta
te
bn
mr
gu
kn
ml
pa
ur
or
as
ne
sa
kok
mai
doi

Rules:
- If text is Hindi written in English letters, return hinglish.
- If text is Urdu script, return ur.
- If text is English, return en.
- Return only the language code.
- Do not explain.

Text:
{text}
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="translation",
            temperature=0
        )

        code = result.strip().lower()

        if code in SUPPORTED_LANGUAGES:
            return code

        return fallback_script_detection(text)

    except Exception:
        return fallback_script_detection(text)