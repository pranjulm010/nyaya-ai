from typing import List, Dict, Any, Optional

from rag.vector_store import get_vector_db


def retrieve_document_context(
    query: str,
    user_id: str = "anonymous",
    document_id: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:

    if not query or not query.strip():
        return []

    print("RETRIEVER QUERY:", query)
    print("RETRIEVER USER_ID:", user_id)
    print("RETRIEVER DOCUMENT_ID:", document_id)
    print("RETRIEVER DOCUMENT_TYPE:", document_type)

    vector_db = get_vector_db()

    raw_results = vector_db.similarity_search_with_score(
        query,
        k=top_k * 5
    )

    print("RAW VECTOR RESULTS:", len(raw_results))

    results = []

    for doc, score in raw_results:
        metadata = doc.metadata or {}

        print("FOUND METADATA:", metadata)

        if metadata.get("user_id") != user_id:
            print("SKIPPED: user_id mismatch")
            continue

        if document_id and metadata.get("document_id") != document_id:
            print("SKIPPED: document_id mismatch")
            continue

        if document_type and metadata.get("document_type") != document_type:
            print("SKIPPED: document_type mismatch")
            continue

        relevance_score = round(
            1 / (1 + float(score)),
            3
        )

        print("RELEVANCE SCORE:", relevance_score)

        if relevance_score < 0.20:
            print("SKIPPED: low relevance")
            continue

        results.append({
            "content": doc.page_content,
            "score": relevance_score,
            "user_id": metadata.get("user_id"),
            "document_id": metadata.get("document_id"),
            "source": metadata.get("source"),
            "document_type": metadata.get("document_type"),
            "page": metadata.get("page"),
            "total_pages": metadata.get("total_pages"),
            "chunk_id": metadata.get("chunk_id"),
        })

        if len(results) >= top_k:
            break

    print("FINAL RETRIEVED RESULTS:", len(results))

    return results