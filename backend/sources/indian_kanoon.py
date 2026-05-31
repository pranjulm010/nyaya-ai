import os
from typing import List, Dict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

KANOON_API_KEY = os.getenv("KANOON_API_KEY")

BASE_URL = "https://api.indiankanoon.org"


def search_indian_kanoon(
    query: str,
    max_results: int = 5
) -> List[Dict]:
    """
    Uses Indian Kanoon API if KANOON_API_KEY exists.
    Falls back to scraping if API key is missing/fails.
    """

    if KANOON_API_KEY:
        api_results = search_indian_kanoon_api(
            query=query,
            max_results=max_results
        )

        if api_results:
            return api_results

    return scrape_indian_kanoon(
        query=query,
        max_results=max_results
    )


def search_indian_kanoon_api(
    query: str,
    max_results: int = 5
) -> List[Dict]:
    try:
        url = f"{BASE_URL}/search/"

        headers = {
            "Authorization": f"Token {KANOON_API_KEY}"
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

        payload = response.json()

        docs = payload.get("docs", [])

        results = []

        for doc in docs[:max_results]:
            results.append({
                "title": doc.get("title", "No Title"),
                "content": doc.get("headline", ""),
                "url": (
                    "https://indiankanoon.org/doc/"
                    + str(doc.get("tid", ""))
                    + "/"
                ) if doc.get("tid") else None,
                "citation": doc.get("citation", ""),
                "court": doc.get("docsource", ""),
                "date": doc.get("publishdate", ""),
                "source": "Indian Kanoon API",
                "relevance_score": 0.85,
                "metadata": doc,
            })

        return results

    except Exception:
        return []


def scrape_indian_kanoon(
    query: str,
    max_results: int = 5
) -> List[Dict]:
    try:
        url = (
            "https://indiankanoon.org/search/?formInput="
            + quote_plus(query)
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for item in soup.select(".result")[:max_results]:
            title_tag = item.select_one(".doc_title a")
            headline_tag = item.select_one(".headline")

            if not title_tag:
                continue

            href = title_tag.get("href", "")

            results.append({
                "title": title_tag.get_text(" ", strip=True),
                "content": headline_tag.get_text(" ", strip=True) if headline_tag else "",
                "url": "https://indiankanoon.org" + href,
                "court": "",
                "citation": "",
                "source": "Indian Kanoon Scrape",
                "relevance_score": 0.7,
            })

        return results

    except Exception:
        return []