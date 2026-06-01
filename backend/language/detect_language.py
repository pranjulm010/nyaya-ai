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


HINGLISH_WORDS = [
    "yeh", "ye", "isko", "iss", "is case",
    "case batao", "case samjhao", "samjhao",
    "batao", "bataiye", "kya", "kaise",
    "kyu", "kyun", "mein", "main",
    "mujhe", "iska", "iski", "kaun",
    "koun", "tha", "hai", "hoga",
    "law", "court", "case", "article",
    "section", "fir", "bail", "ipc", "crpc",
]


def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"

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

    lower_text = text.lower()

    if any(word in lower_text for word in HINGLISH_WORDS):
        return "hinglish"

    return "en"