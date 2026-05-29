from datetime import datetime


# =========================================
# IN-MEMORY STORAGE
# =========================================
chat_memory = []


# =========================================
# SAVE MEMORY
# =========================================
def save_memory(
    role,
    content,
    session_id="default",
    user_id="anonymous"
):

    try:

        memory_item = {

            "role": role,

            "content": content,

            "timestamp":
            datetime.utcnow().isoformat(),

            "session_id":
            session_id,

            "user_id":
            user_id
        }

        chat_memory.append(
            memory_item
        )

        # =============================
        # LIMIT MEMORY SIZE
        # =============================
        MAX_MEMORY = 50

        if len(chat_memory) > MAX_MEMORY:

            del chat_memory[0]

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================
# GET FULL MEMORY
# =========================================
def get_memory(
    session_id="default",
    user_id="anonymous",
    limit=10
):

    try:

        filtered_memory = [

            memory
            for memory in chat_memory

            if (
                memory["session_id"]
                == session_id
                and
                memory["user_id"]
                == user_id
            )
        ]

        recent_memory = (
            filtered_memory[-limit:]
        )

        return recent_memory

    except Exception as e:

        return [{
            "error": str(e)
        }]


# =========================================
# FORMAT MEMORY
# =========================================
def format_memory(memory_list):

    formatted = ""

    for memory in memory_list:

        role = memory.get(
            "role",
            "unknown"
        )

        content = memory.get(
            "content",
            ""
        )

        timestamp = memory.get(
            "timestamp",
            ""
        )

        formatted += f"""

ROLE:
{role}

TIME:
{timestamp}

CONTENT:
{content}

==========================
"""

    return formatted


# =========================================
# SEARCH MEMORY
# =========================================
def search_memory(
    query,
    session_id="default",
    user_id="anonymous",
    limit=5
):

    try:

        memories = get_memory(
            session_id=session_id,
            user_id=user_id,
            limit=50
        )

        relevant_memories = []

        query_words = set(
            query.lower().split()
        )

        for memory in memories:

            content = memory.get(
                "content",
                ""
            )

            content_words = set(
                content.lower().split()
            )

            # simple relevance
            common_words = (
                query_words.intersection(
                    content_words
                )
            )

            if len(common_words) > 0:

                relevant_memories.append(
                    memory
                )

        relevant_memories = (
            relevant_memories[-limit:]
        )

        return relevant_memories

    except Exception as e:

        return [{
            "error": str(e)
        }]