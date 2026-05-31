from typing import List, Dict, Any

from memory.chat_history import (
    save_message,
    get_history
)


def save_chat_message(
    user_id: str,
    session_id: str,
    role: str,
    content: str
) -> None:
    """
    Save user/assistant message.
    """

    save_message(
        user_id=user_id,
        session_id=session_id,
        role=role,
        content=content
    )


def get_chat_history(
    user_id: str,
    session_id: str,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Get chat history.
    """

    return get_history(
        user_id=user_id,
        session_id=session_id,
        limit=limit
    )


def get_relevant_memory(
    query: str,
    user_id: str,
    session_id: str,
    limit: int = 3
) -> List[Dict[str, Any]]:
    """
    Cheap memory retrieval.

    Returns relevant previous chat messages.
    Used for conversational continuity.

    Example:
    User:
    "summarize previous case"

    AI remembers previous case.
    """

    history = get_history(
        user_id=user_id,
        session_id=session_id,
        limit=20
    )

    if not history:
        return []

    query_words = set(
        query.lower().split()
    )

    relevant_memories = []

    for msg in reversed(history):

        content = msg.get(
            "content",
            ""
        )

        if not content:
            continue

        content_words = set(
            content.lower().split()
        )

        overlap = query_words.intersection(
            content_words
        )

        if len(overlap) >= 1:

            relevant_memories.append({
                "source_type": "memory",
                "source_name": "Chat Memory",
                "title": "Previous Conversation",
                "content": content,
                "trust_score": 0.4,
                "relevance_score": 0.5,
                "metadata": {
                    "role": msg.get("role")
                }
            })

        if len(relevant_memories) >= limit:
            break

    return relevant_memories