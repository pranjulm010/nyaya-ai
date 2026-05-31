import re


def mask_pii(text: str) -> str:
    if not text:
        return ""

    text = str(text)

    text = re.sub(r"\b\d{12}\b", "[AADHAAR_MASKED]", text)
    text = re.sub(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", "[PAN_MASKED]", text)
    text = re.sub(r"\b\d{10}\b", "[PHONE_MASKED]", text)
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL_MASKED]", text)

    return text