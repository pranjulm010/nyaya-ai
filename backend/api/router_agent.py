from .pdf_agent import pdf_agent
from .kanoon_agent import kanoon_agent
from .memory_agent import (
    search_memory,
    format_memory,
    get_memory
)
from .drafting_agent import drafting_agent
from .webscrap_agent import ask_web_agent


def router_agent(user_query):

    collected_context = []

    # =========================================
    # 1. MEMORY CONTEXT
    # =========================================
    try:

        memory = get_memory()

        if memory:

            collected_context.append(f"""
            PREVIOUS CHAT HISTORY:
            {memory}
            """)

    except Exception as e:

        collected_context.append(
            f"MEMORY ERROR:\n{str(e)}"
        )

    # =========================================
    # 2. PDF VECTOR SEARCH (ALWAYS)
    # =========================================
    try:

        pdf_context = search_context(
            user_query,
            top_k=5
        )

        if pdf_context:

            collected_context.append(f"""
            PDF KNOWLEDGE BASE:
            {pdf_context}
            """)

    except Exception as e:

        collected_context.append(
            f"PDF SEARCH ERROR:\n{str(e)}"
        )

    # =========================================
    # 3. PDF AGENT
    # =========================================
    try:

        pdf_analysis = pdf_agent(
            user_query
        )

        if pdf_analysis:

            collected_context.append(f"""
            PDF AGENT ANALYSIS:
            {pdf_analysis}
            """)

    except Exception as e:

        collected_context.append(
            f"PDF AGENT ERROR:\n{str(e)}"
        )

    # =========================================
    # 4. LEGAL / KANOON AGENT
    # =========================================
    legal_keywords = [
        "case",
        "judgment",
        "legal",
        "law",
        "section",
        "article",
        "court",
        "petition",
        "bail",
        "ipc",
        "constitution",
        "advocate",
        "criminal",
        "civil",
        "supreme court",
        "high court"
    ]

    if any(
        word in user_query.lower()
        for word in legal_keywords
    ):

        try:

            kanoon_data = kanoon_agent(
                user_query
            )

            if kanoon_data:

                collected_context.append(f"""
                INDIAN LEGAL DATABASE:
                {kanoon_data}
                """)

        except Exception as e:

            collected_context.append(
                f"KANOON AGENT ERROR:\n{str(e)}"
            )

    # =========================================
    # 5. WEB SEARCH / SCRAPER AGENT
    # =========================================
    web_keywords = [
        "latest",
        "news",
        "today",
        "current",
        "recent",
        "website",
        "online",
        "update"
    ]

    if (
        "http" in user_query
        or "www" in user_query
        or any(
            word in user_query.lower()
            for word in web_keywords
        )
    ):

        try:

            web_data = ask_web_agent(
                user_query
            )

            if web_data:

                collected_context.append(f"""
                WEB RESEARCH:
                {web_data}
                """)

        except Exception as e:

            collected_context.append(
                f"WEB AGENT ERROR:\n{str(e)}"
            )

    # =========================================
    # 6. FINAL COMBINED CONTEXT
    # =========================================
    combined_context = "\n\n".join(
        collected_context
    )

    # =========================================
    # 7. FINAL MASTER PROMPT
    # =========================================
    final_prompt = f"""
You are Nyaya AI,
an advanced Indian Legal AI Assistant.

=========================================
USER QUESTION
=========================================

{user_query}

=========================================
AVAILABLE CONTEXT
=========================================

{combined_context}

=========================================
YOUR RESPONSIBILITIES
=========================================

1. Answer accurately using provided context
2. Prioritize PDF knowledge if available
3. Use legal reasoning when needed
4. Combine web + kanoon + pdf knowledge
5. Mention uncertainty clearly
6. Do not hallucinate laws or judgments
7. Keep answers structured and professional
8. If multiple sources conflict:
   - mention the conflict
   - explain which source is stronger

=========================================
RESPONSE FORMAT
=========================================

- Summary
- Key Findings
- Legal Analysis
- Important Notes
- Final Conclusion
"""

    # =========================================
    # 8. FINAL AI RESPONSE
    # =========================================
    try:

        final_answer = drafting_agent(
            final_prompt
        )

        return final_answer

    except Exception as e:

        return f"""
FINAL DRAFTING ERROR:

{str(e)}
"""