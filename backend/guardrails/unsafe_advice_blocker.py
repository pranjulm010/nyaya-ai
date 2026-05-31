UNSAFE_PATTERNS = [
    "hide evidence",
    "destroy evidence",
    "delete evidence",
    "forge",
    "fake document",
    "fake affidavit",
    "false statement",
    "lie in court",
    "mislead court",
    "bribe",
    "bribery",
    "evade law",
    "threaten witness",
    "tamper witness",
    "fabricate evidence",
    "create fake proof",
    "backdate document",
    "manipulate evidence",
]


def is_unsafe_query(query: str) -> bool:
    if not query:
        return False

    q = query.lower()

    return any(pattern in q for pattern in UNSAFE_PATTERNS)