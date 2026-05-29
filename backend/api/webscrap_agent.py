import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote

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
# HEADERS
# =========================================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


# =========================================
# LEGAL SOURCES
# =========================================
LEGAL_SOURCES = [

    # Indian Kanoon
    {
        "name": "Indian Kanoon",
        "search_url":
        "https://indiankanoon.org/search/?formInput="
    },

    # LiveLaw
    {
        "name": "LiveLaw",
        "search_url":
        "https://www.livelaw.in/search?query="
    },

    # Bar and Bench
    {
        "name": "Bar and Bench",
        "search_url":
        "https://www.barandbench.com/search?q="
    },

    # PRS India
    {
        "name": "PRS India",
        "search_url":
        "https://prsindia.org/search/node/"
    },
]


# =========================================
# CLEAN TEXT
# =========================================
def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================
# SCRAPE PAGE
# =========================================
def scrape_page(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # remove junk
        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "svg"
        ]):
            tag.decompose()

        title = (
            soup.title.string.strip()
            if soup.title
            else "No Title"
        )

        paragraphs = soup.find_all("p")

        content = " ".join([
            p.get_text(" ", strip=True)
            for p in paragraphs[:50]
        ])

        content = clean_text(content)

        return {
            "success": True,
            "url": url,
            "title": title,
            "content": content[:5000]
        }

    except Exception as e:

        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


# =========================================
# SEARCH LEGAL SOURCES
# =========================================
def search_legal_sources(query):

    results = []

    for source in LEGAL_SOURCES:

        try:

            search_url = (
                source["search_url"]
                + quote(query)
            )

            scraped = scrape_page(
                search_url
            )

            if scraped["success"]:

                results.append({
                    "source": source["name"],
                    "url": scraped["url"],
                    "title": scraped["title"],
                    "content": scraped["content"]
                })

        except:
            continue

    return results


# =========================================
# FILTER RELEVANT RESULTS
# =========================================
def filter_relevant_results(
    query,
    results
):

    if not results:
        return []

    combined = ""

    for idx, result in enumerate(results):

        combined += f"""

RESULT {idx+1}

SOURCE:
{result['source']}

TITLE:
{result['title']}

CONTENT:
{result['content'][:2000]}

==================================
"""

    prompt = f"""
You are a Legal Research AI.

USER QUERY:
{query}

LEGAL SEARCH RESULTS:
{combined}

TASK:
1. Select only highly relevant results
2. Ignore unrelated legal content
3. Extract important legal insights
4. Keep citations/source names
5. Return concise structured summary
"""

    response = llm.invoke(prompt)

    return response.content


# =========================================
# MAIN WEB AGENT
# =========================================
def ask_web_agent(query):

    try:

        # =================================
        # SEARCH SOURCES
        # =================================
        results = search_legal_sources(
            query
        )

        if not results:

            return """
No relevant legal web results found.
"""

        # =================================
        # FILTER + SUMMARIZE
        # =================================
        final_answer = (
            filter_relevant_results(
                query,
                results
            )
        )

        return final_answer

    except Exception as e:

        return f"""
WEB AGENT ERROR:

{str(e)}
"""