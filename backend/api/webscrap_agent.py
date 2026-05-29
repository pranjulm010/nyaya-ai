import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# =========================
# LOAD ENV
# =========================
load_dotenv()


# =========================
# LLM
# =========================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# =========================
# HEADERS
# =========================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


# =========================
# WEBSITES TO SEARCH
# =========================
TARGET_SITES = [

    # Supreme Court
    "https://www.sci.gov.in",

    # High Courts
    "https://www.allahabadhighcourt.in",
    "https://delhihighcourt.nic.in",
    "https://bombayhighcourt.nic.in",
    "https://www.hcmadras.tn.nic.in",
    "https://karnatakajudiciary.kar.nic.in",

    # Legal Research
    "https://indiankanoon.org",
    "https://www.livelaw.in",
    "https://www.barandbench.com",
    "https://prsindia.org",
]


# =========================
# SCRAPE WEBSITE
# =========================
def scrape_website(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # remove junk tags
        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        clean_text = " ".join(text.split())

        title = (
            soup.title.string.strip()
            if soup.title
            else "No Title"
        )

        return {
            "success": True,
            "title": title,
            "content": clean_text[:3000]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================
# SEARCH MULTIPLE SITES
# =========================
def search_websites(query):

    all_results = []

    for site in TARGET_SITES:

        try:

            search_url = (
                f"{site}/search/?formInput="
                f"{quote(query)}"
            )

            result = scrape_website(
                search_url
            )

            if result["success"]:

                all_results.append({
                    "website": site,
                    "title": result["title"],
                    "content": result["content"]
                })

        except:
            continue

    return all_results


# =========================
# MAIN WEB AGENT
# =========================
def ask_web_agent(query):

    try:

        web_results = search_websites(
            query
        )

        if not web_results:

            return "No web results found."

        combined_data = ""

        for result in web_results:

            combined_data += f"""
            WEBSITE:
            {result['website']}

            TITLE:
            {result['title']}

            CONTENT:
            {result['content']}

            =====================
            """

        final_prompt = f"""
        You are Nyaya AI Web Research Agent.

        USER QUERY:
        {query}

        WEB DATA:
        {combined_data}

        TASK:
        - analyze information
        - summarize findings
        - extract legal insights
        - compare information
        - provide final answer
        """

        response = llm.invoke(
            final_prompt
        )

        return response.content

    except Exception as e:

        return f"""
        WEB AGENT ERROR:
        {str(e)}
        """