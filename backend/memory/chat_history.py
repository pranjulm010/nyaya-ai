from typing import List, Dict, Any

# Temporary in-memory storage
# Later replace with Redis/Postgres

CHAT_HISTORY_DB = {}


def save_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
) -> None:

    key = f"{user_id}:{session_id}"

    if key not in CHAT_HISTORY_DB:
        CHAT_HISTORY_DB[key] = []

    CHAT_HISTORY_DB[key].append({
        "role": role,
        "content": content
    })


def get_history(
    user_id: str,
    session_id: str,
    limit: int = 20
) -> List[Dict[str, Any]]:

    key = f"{user_id}:{session_id}"

    messages = CHAT_HISTORY_DB.get(
        key,
        []
    )

    return messages[-limit:]


def clear_history(
    user_id: str,
    session_id: str
) -> None:

    key = f"{user_id}:{session_id}"

    if key in CHAT_HISTORY_DB:
        del CHAT_HISTORY_DB[key]