from typing import Literal


SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "en": "English",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
}


def detect_language(text: str) -> str:
    if not text:
        return "en"

    for char in text:
        code = ord(char)

        # Hindi / Marathi
        if 0x0900 <= code <= 0x097F:
            return "hi"

        # Bengali
        if 0x0980 <= code <= 0x09FF:
            return "bn"

        # Punjabi
        if 0x0A00 <= code <= 0x0A7F:
            return "pa"

        # Gujarati
        if 0x0A80 <= code <= 0x0AFF:
            return "gu"

        # Tamil
        if 0x0B80 <= code <= 0x0BFF:
            return "ta"

        # Telugu
        if 0x0C00 <= code <= 0x0C7F:
            return "te"

        # Kannada
        if 0x0C80 <= code <= 0x0CFF:
            return "kn"

        # Malayalam
        if 0x0D00 <= code <= 0x0D7F:
            return "ml"

        # Urdu / Arabic script
        if 0x0600 <= code <= 0x06FF:
            return "ur"

    return "en"