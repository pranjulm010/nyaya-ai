from typing import List, Dict
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_bar_and_bench(query: str, max_results: int = 5) -> List[Dict]:
    try:
        search_query = f"site:barandbench.com {query}"
        url = f"https://duckduckgo.com/html/?q={quote_plus(search_query)}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for item in soup.select(".result")[:max_results]:
            title_tag = item.select_one(".result__title a")
            snippet_tag = item.select_one(".result__snippet")

            if not title_tag:
                continue

            results.append({
                "title": title_tag.get_text(" ", strip=True),
                "content": snippet_tag.get_text(" ", strip=True) if snippet_tag else "",
                "url": title_tag.get("href"),
                "source": "Bar and Bench",
                "relevance_score": 0.6
            })

        return results

    except Exception:
        return []