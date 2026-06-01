import unicodedata


def detect_language(text: str) -> str:
    """
    Returns 'hindi' if the text contains Devanagari script characters,
    otherwise returns 'english'.
    """
    for char in text:
        if unicodedata.category(char) in ("Lo", "Mn", "Mc"):
            block = ord(char)
            # Devanagari Unicode block: U+0900–U+097F
            if 0x0900 <= block <= 0x097F:
                return "hindi"
    return "english"


LANGUAGE_INSTRUCTION = {
    "hindi": (
        "IMPORTANT: The user asked their question in Hindi. "
        "You MUST respond entirely in Hindi (Devanagari script). "
        "All headings, explanations, legal terms, and conclusions must be in Hindi. "
        "You may include English legal citations (like IPC Section numbers or case names) "
        "inside your Hindi response where necessary."
    ),
    "english": "",
}
