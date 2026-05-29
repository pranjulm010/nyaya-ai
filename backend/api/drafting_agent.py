from dotenv import load_dotenv

from langchain_groq import ChatGroq


# =========================================
# LOAD ENV
# =========================================
load_dotenv()


# =========================================
# LLM
# =========================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# =========================================
# FORMAT SOURCES
# =========================================
def extract_sources(context):

    sources = []

    if "PDF KNOWLEDGE BASE" in context:
        sources.append("PDF Documents")

    if "INDIAN LEGAL DATABASE" in context:
        sources.append("Indian Kanoon")

    if "WEB RESEARCH" in context:
        sources.append("Legal Web Sources")

    if "PREVIOUS CHAT HISTORY" in context:
        sources.append("Conversation Memory")

    return sources


# =========================================
# DRAFTING AGENT
# =========================================
def drafting_agent(prompt):

    try:

        # =================================
        # EXTRACT SOURCES
        # =================================
        sources = extract_sources(
            prompt
        )

        source_text = ", ".join(
            sources
        )

        # =================================
        # STRICT SYSTEM PROMPT
        # =================================
        strict_prompt = f"""
You are Nyaya AI,
an advanced Indian Legal AI Assistant.

====================================
STRICT INSTRUCTIONS
====================================

1. Use ONLY provided context
2. Never hallucinate
3. Never invent laws or judgments
4. Never assume facts
5. If information is missing,
   clearly say so
6. Prefer PDF evidence first
7. Prefer court/legal sources
   over web articles
8. Mention uncertainty honestly
9. Keep answers professional
10. Mention important legal risks
11. Mention source conflicts
    if present

====================================
AVAILABLE SOURCES
====================================

{source_text}

====================================
CONTEXT PROVIDED
====================================

{prompt}

====================================
RESPONSE FORMAT
====================================

# Summary

# Key Findings

# Legal Analysis

# Important Clauses / Judgments

# Risks / Missing Information

# Final Conclusion

# Sources Used

====================================
IMPORTANT
====================================

If answer is unavailable in context,
respond exactly:

"I could not find this information
in the provided sources."
"""

        # =================================
        # GENERATE RESPONSE
        # =================================
        response = llm.invoke(
            strict_prompt
        )

        final_answer = (
            response.content
        )

        # =================================
        # EMPTY RESPONSE SAFETY
        # =================================
        if not final_answer.strip():

            return """
No response generated.
"""

        return final_answer

    except Exception as e:

        return f"""
DRAFTING AGENT ERROR:

{str(e)}
"""