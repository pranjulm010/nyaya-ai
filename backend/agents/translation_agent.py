from typing import Dict, Any

from language.detect_language import detect_language
from language.translate_to_english import translate_to_english
from language.translate_to_user_language import translate_to_user_language
from language.regional_prompts import (
    get_language_name,
    get_language_instruction,
    detect_explicit_response_language,
)


def translate_query_if_needed(
    query: str,
    intent_data: Dict[str, Any] | None = None,
) -> Dict[str, Any]:

    original_language = detect_language(query)
    explicit_language = detect_explicit_response_language(query)

    target_language = explicit_language or original_language

    if original_language == "en":
        english_query = query
        translated = False
    else:
        english_query = translate_to_english(
            text=query,
            source_language=original_language,
        )
        translated = english_query.strip().lower() != query.strip().lower()

    return {
        "original_query": query,
        "query": english_query,
        "english_query": english_query,
        "original_language": original_language,
        "original_language_name": get_language_name(original_language),
        "explicit_response_language": explicit_language,
        "target_language": target_language,
        "target_language_name": get_language_name(target_language),
        "translated": translated,
        "language_instruction": get_language_instruction(target_language),
    }


def translate_answer_if_needed(
    answer_payload: Dict[str, Any],
    target_language: str,
) -> Dict[str, Any]:

    if target_language == "en":
        answer_payload["language"] = "en"
        answer_payload["translated"] = False
        return answer_payload

    answer = answer_payload.get("answer", "")

    if not answer:
        answer_payload["language"] = target_language
        answer_payload["translated"] = False
        return answer_payload

    translated_answer = translate_to_user_language(
        text=answer,
        target_language=target_language,
    )

    answer_payload["answer"] = translated_answer
    answer_payload["language"] = target_language
    answer_payload["translated"] = translated_answer.strip() != answer.strip()

    return answer_payload