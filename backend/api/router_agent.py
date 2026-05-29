from .pdf_agent import pdf_agent
from .kanoon_agent import kanoon_agent
from .memory_agent import get_memory
from .drafting_agent import drafting_agent
from .webscrap_agent import ask_web_agent


def router_agent(user_query):

    final_context = []

    # =========================
    # MEMORY
    # =========================
    try:

        memory = get_memory()

        final_context.append(f"""
        CHAT HISTORY:
        {memory}
        """)

    except Exception as e:

        final_context.append(
            f"MEMORY ERROR: {str(e)}"
        )

    # =========================
    # PDF AGENT
    # =========================
    if any(word in user_query.lower() for word in [
        "pdf",
        "document",
        "agreement",
        "contract",
        "file",
        "upload"
    ]):

        try:

            pdf_context = pdf_agent(
                user_query
            )

            final_context.append(f"""
            PDF CONTEXT:
            {pdf_context}
            """)

        except Exception as e:

            final_context.append(
                f"PDF AGENT ERROR: {str(e)}"
            )

    # =========================
    # KANOON AGENT
    # =========================
    if any(word in user_query.lower() for word in [
        "case",
        "judgment",
        "supreme court",
        "high court",
        "legal",
        "law",
        "section",
        "article"
    ]):

        try:

            kanoon_data = kanoon_agent(
                user_query
            )

            final_context.append(f"""
            KANOON DATA:
            {kanoon_data}
            """)

        except Exception as e:

            final_context.append(
                f"KANOON AGENT ERROR: {str(e)}"
            )

    # =========================
    # WEBSCRAPER AGENT
    # =========================
    if (
        "http" in user_query
        or "www" in user_query
        or "website" in user_query.lower()
        or "latest" in user_query.lower()
        or "news" in user_query.lower()
        or "online" in user_query.lower()
    ):

        try:

            web_data = ask_webscraper_agent(
                user_query
            )

            final_context.append(f"""
            WEBSCRAPER DATA:
            {web_data}
            """)

        except Exception as e:

            final_context.append(
                f"WEBSCRAPER AGENT ERROR: {str(e)}"
            )

    # =========================
    # COMBINE CONTEXT
    # =========================
    combined_context = "\n\n".join(
        final_context
    )

    # =========================
    # FINAL PROMPT
    # =========================
    final_prompt = f"""
    You are Nyaya AI,
    an advanced Indian Legal AI Assistant.

    Your role:
    - answer legal questions
    - summarize documents
    - analyze judgments
    - use web research
    - combine outputs from multiple AI agents
    - provide accurate reasoning

    AVAILABLE CONTEXT:
    {combined_context}

    USER QUESTION:
    {user_query}

    IMPORTANT INSTRUCTIONS:
    - Give structured responses
    - Use headings when needed
    - Mention legal reasoning
    - Use all relevant context
    - Do not hallucinate
    - If data is unavailable, say so clearly
    - Keep response professional
    """

    # =========================
    # FINAL DRAFTING AGENT
    # =========================
    try:

        answer = drafting_agent(
            final_prompt
        )

        return answer

    except Exception as e:

        return f"""
        FINAL DRAFTING ERROR:
        {str(e)}
        """