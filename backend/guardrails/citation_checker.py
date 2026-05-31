from typing import List, Dict, Any


def citation_checker(
    sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    checked_sources = []

    for source in sources:
        item = dict(source)

        source_type = item.get("source_type")

        has_document_reference = (
            source_type in ["document", "pdf"]
            and (
                item.get("page") is not None
                or item.get("metadata", {}).get("document_id")
            )
        )

        has_url = bool(item.get("url"))
        has_citation = bool(item.get("citation"))
        has_source_name = bool(item.get("source_name"))

        item["citation_verified"] = any([
            has_document_reference,
            has_url,
            has_citation,
            has_source_name,
        ])

        if item["citation_verified"]:
            checked_sources.append(item)

    return checked_sources