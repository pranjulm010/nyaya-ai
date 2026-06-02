from typing import List, Dict
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from sources.llm_source_helper import (
    enrich_result_with_llm,
    sort_and_limit_results,
)


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def search_supreme_court(query: str, max_results: int = 5) -> List[Dict]:
    return scrape_supreme_court(query, max_results)


def scrape_supreme_court(query: str, max_results: int = 5) -> List[Dict]:
    try:
        search_query = f"site:sci.gov.in {query}"
        url = f"https://duckduckgo.com/html/?q={quote_plus(search_query)}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for item in soup.select(".result")[:max_results * 2]:
            title_tag = item.select_one(".result__title a")
            snippet_tag = item.select_one(".result__snippet")

            if not title_tag:
                continue

            result = {
                "title": title_tag.get_text(" ", strip=True),
                "content": snippet_tag.get_text(" ", strip=True) if snippet_tag else "",
                "url": title_tag.get("href"),
                "court": "Supreme Court of India",
                "source": "Supreme Court of India",
            }

            result = enrich_result_with_llm(query=query, result=result)

            if result["relevance_score"] >= 0.45:
                results.append(result)

        return sort_and_limit_results(results, max_results)

    except Exception:
        return []