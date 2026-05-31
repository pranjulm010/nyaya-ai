from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from rag.embeddings import get_embedding_model
from core.config import CHROMA_DIR


_vector_db = None


def get_vector_db():
    global _vector_db

    if _vector_db is None:
        _vector_db = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=get_embedding_model()
        )

    return _vector_db


def store_document_chunks(
    chunks: List[Dict[str, Any]],
    user_id: str,
    document_id: str
) -> Dict[str, Any]:

    try:
        print("VECTOR STORE: chunks received:", len(chunks))

        if not chunks:
            return {
                "success": False,
                "error": "No chunks to store."
            }

        documents = []

        for chunk in chunks:
            content = chunk.get("content", "")

            if not content.strip():
                continue

            metadata = {
                "user_id": user_id,
                "document_id": document_id,
                "source": chunk.get("source"),
                "document_type": chunk.get("document_type"),
                "page": chunk.get("page"),
                "total_pages": chunk.get("total_pages"),
                "chunk_id": chunk.get("chunk_id"),
            }

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

        print("VECTOR STORE: documents prepared:", len(documents))

        vector_db = get_vector_db()

        if documents:
            vector_db.add_documents(documents)

        print("VECTOR DB STORED:", len(documents))

        return {
            "success": True,
            "stored_chunks": len(documents)
        }

    except Exception as error:
        print("VECTOR STORE ERROR:", error)
        return {
            "success": False,
            "error": str(error)
        }