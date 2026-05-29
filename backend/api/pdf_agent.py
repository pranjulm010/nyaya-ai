from .rag import search_documents

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
# FORMAT DOCUMENTS
# =========================================
def format_documents(documents):

    formatted_text = ""

    for idx, doc in enumerate(documents):

        content = doc.get(
            "content",
            ""
        )

        page = doc.get(
            "page",
            "Unknown"
        )

        source = doc.get(
            "source",
            "Unknown PDF"
        )

        formatted_text += f"""

DOCUMENT CHUNK {idx+1}

SOURCE:
{source}

PAGE:
{page}

CONTENT:
{content}

====================================
"""

    return formatted_text


# =========================================
# PDF AGENT
# =========================================
def pdf_agent(query):

    try:

        # =================================
        # SEARCH VECTOR DATABASE
        # =================================
        documents = search_documents(
            query=query,
            top_k=5
        )

        # =================================
        # NO DOCUMENTS FOUND
        # =================================
        if not documents:

            return """
No relevant PDF context found.
"""

        # =================================
        # FORMAT DOCUMENTS
        # =================================
        formatted_context = (
            format_documents(
                documents
            )
        )

        # =================================
        # FINAL PROMPT
        # =================================
        final_prompt = f"""
You are Nyaya AI PDF Analysis Agent.

====================================
USER QUERY
====================================

{query}

====================================
PDF RETRIEVED CONTEXT
====================================

{formatted_context}

====================================
TASK
====================================

1. Analyze the PDF context carefully
2. Extract important legal information
3. Summarize relevant findings
4. Mention important clauses if present
5. Mention page references when possible
6. If context is insufficient,
   clearly say so
7. Do not hallucinate
8. Keep answer concise but useful
"""

        # =================================
        # LLM ANALYSIS
        # =================================
        response = llm.invoke(
            final_prompt
        )

        return response.content

    except Exception as e:

        return f"""
PDF AGENT ERROR:

{str(e)}
"""