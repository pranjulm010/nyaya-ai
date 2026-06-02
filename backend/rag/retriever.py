from typing import List, Dict, Any, Optional

from rag.vector_store import get_vector_db
from core.llm_router import run_llm


def llm_chunk_relevance_score(
    query: str,
    content: str
) -> float:
    prompt = f"""
You are a legal document relevance evaluator.

User question:
{query}

Document chunk:
{content[:2500]}

Give relevance score from 0 to 1.

Rules:
- 1.0 = directly answers the question
- 0.7 = useful but partial
- 0.4 = weakly related
- 0.0 = unrelated

Return only a number.
"""

    try:
        result = run_llm(
            prompt=prompt,
            intent="document_question",
            temperature=0
        )

        score = float(result.strip())

        if score < 0:
            return 0.0

        if score > 1:
            return 1.0

        return round(score, 3)

    except Exception:
        return 0.5


def retrieve_document_context(
    query: str,
    user_id: str = "anonymous",
    document_id: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 5,
    use_llm_reranking: bool = True
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

    candidates = []

    for doc, score in raw_results:
        metadata = doc.metadata or {}

        if metadata.get("user_id") != user_id:
            continue

        if document_id and metadata.get("document_id") != document_id:
            continue

        if document_type and metadata.get("document_type") != document_type:
            continue

        vector_score = round(
            1 / (1 + float(score)),
            3
        )

        if vector_score < 0.20:
            continue

        item = {
            "content": doc.page_content,
            "score": vector_score,
            "vector_score": vector_score,
            "llm_score": None,
            "user_id": metadata.get("user_id"),
            "document_id": metadata.get("document_id"),
            "source": metadata.get("source"),
            "document_type": metadata.get("document_type"),
            "page": metadata.get("page"),
            "total_pages": metadata.get("total_pages"),
            "chunk_id": metadata.get("chunk_id"),
        }

        candidates.append(item)

    print("VECTOR FILTERED CANDIDATES:", len(candidates))

    if use_llm_reranking:
        for item in candidates:
            item["llm_score"] = llm_chunk_relevance_score(
                query=query,
                content=item["content"]
            )

            item["score"] = round(
                item["vector_score"] * 0.4
                + item["llm_score"] * 0.6,
                3
            )

    candidates = sorted(
        candidates,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    results = candidates[:top_k]

    print("FINAL RETRIEVED RESULTS:", len(results))

    return results