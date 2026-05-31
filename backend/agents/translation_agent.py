from typing import Dict, Any

from language.detect_language import detect_language
from core.llm import get_llm


def translate_query_if_needed(
    query: str,
    intent_data: Dict[str, Any]
) -> Dict[str, Any]:

    language = detect_language(query)

    if language == "en":
        return {
            "query": query,
            "original_language": "en",
        }

    try:
        llm = get_llm()

        prompt = f"""
Translate the following legal query to English.

Rules:
- Preserve legal meaning.
- Preserve case names and sections.
- Return only translated text.

Query:
{query}
"""

        response = llm.invoke(prompt)

        translated_query = response.content.strip()

        print("TRANSLATED QUERY:", translated_query)

        return {
            "query": translated_query,
            "original_language": language,
        }

    except Exception as error:
        print("TRANSLATION ERROR:", error)

        return {
            "query": query,
            "original_language": language,
        }


def translate_answer_if_needed(
    answer_payload: Dict[str, Any],
    target_language: str
) -> Dict[str, Any]:

    if target_language == "en":
        return answer_payload

    try:
        llm = get_llm()

        answer = answer_payload.get("answer", "")

        prompt = f"""
Translate this legal answer into {target_language}.

Rules:
- Use simple regional language.
- Preserve legal citations.
- Preserve section names.
- Preserve court names.
- Preserve case names.

Answer:
{answer}
"""

        response = llm.invoke(prompt)

        translated_answer = response.content.strip()

        answer_payload["answer"] = translated_answer

        return answer_payload

    except Exception as error:
        print("ANSWER TRANSLATION ERROR:", error)
        return answer_payload