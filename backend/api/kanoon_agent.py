import os
import requests

from dotenv import load_dotenv

from langchain_groq import ChatGroq


# =========================================
# LOAD ENV
# =========================================
load_dotenv()


# =========================================
# API KEY
# =========================================
API_KEY = os.getenv(
    "KANOON_API_KEY"
)


# =========================================
# LLM
# =========================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# =========================================
# BASE URL
# =========================================
BASE_URL = (
    "https://api.indiankanoon.org"
)


# =========================================
# SEARCH INDIAN KANOON
# =========================================
def search_kanoon(
    query,
    max_results=5
):

    try:

        url = (
            f"{BASE_URL}/search/"
        )

        headers = {
            "Authorization":
            f"Token {API_KEY}"
        }

        data = {
            "formInput": query
        }

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

        docs = result.get(
            "docs",
            []
        )

        formatted_results = []

        for doc in docs[:max_results]:

            formatted_results.append({

                "title":
                doc.get(
                    "title",
                    "No Title"
                ),

                "headline":
                doc.get(
                    "headline",
                    ""
                ),

                "docsource":
                doc.get(
                    "docsource",
                    ""
                ),

                "publishdate":
                doc.get(
                    "publishdate",
                    ""
                ),

                "citation":
                doc.get(
                    "citation",
                    ""
                ),

                "court":
                doc.get(
                    "docsource",
                    ""
                )
            })

        return {
            "success": True,
            "results":
            formatted_results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================
# FORMAT RESULTS
# =========================================
def format_kanoon_results(
    results
):

    formatted = ""

    for idx, item in enumerate(results):

        formatted += f"""

CASE {idx+1}

TITLE:
{item.get('title')}

COURT:
{item.get('court')}

CITATION:
{item.get('citation')}

DATE:
{item.get('publishdate')}

HEADLINE:
{item.get('headline')}

====================================
"""

    return formatted


# =========================================
# MAIN KANOON AGENT
# =========================================
def kanoon_agent(query):

    try:

        # =================================
        # SEARCH CASES
        # =================================
        search_result = search_kanoon(
            query=query,
            max_results=5
        )

        if not search_result["success"]:

            return f"""
KANOON SEARCH ERROR:

{search_result['error']}
"""

        results = search_result.get(
            "results",
            []
        )

        if not results:

            return """
No relevant legal judgments found.
"""

        # =================================
        # FORMAT RESULTS
        # =================================
        formatted_cases = (
            format_kanoon_results(
                results
            )
        )

        # =================================
        # FINAL PROMPT
        # =================================
        final_prompt = f"""
You are Nyaya AI Legal Research Agent.

====================================
USER QUERY
====================================

{query}

====================================
INDIAN KANOON RESULTS
====================================

{formatted_cases}

====================================
TASK
====================================

1. Analyze the legal judgments
2. Extract important legal principles
3. Summarize relevant rulings
4. Mention important precedents
5. Mention court names
6. Mention citations if relevant
7. Avoid hallucination
8. If results are weak,
   clearly mention uncertainty
"""

        # =================================
        # AI ANALYSIS
        # =================================
        response = llm.invoke(
            final_prompt
        )

        return response.content

    except Exception as e:

        return f"""
KANOON AGENT ERROR:

{str(e)}
"""