from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    Chroma
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain.schema import Document


# =========================================
# EMBEDDING MODEL
# =========================================
embedding = HuggingFaceEmbeddings(
    model_name=(
        "sentence-transformers/"
        "all-MiniLM-L6-v2"
    )
)


# =========================================
# VECTOR DATABASE
# =========================================
vector_db = Chroma(
    persist_directory="legal_db",
    embedding_function=embedding
)


# =========================================
# TEXT SPLITTER
# =========================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# =========================================
# STORE DOCUMENT
# =========================================
def store_document(pdf_data):

    """
    pdf_data format:

    {
        "chunks": [
            {
                "content": "...",
                "page": 1,
                "source": "agreement.pdf"
            }
        ]
    }
    """

    try:

        documents = []

        chunks = pdf_data.get(
            "chunks",
            []
        )

        for chunk in chunks:

            content = chunk.get(
                "content",
                ""
            )

            if not content.strip():
                continue

            # =============================
            # SPLIT INTO SMALLER CHUNKS
            # =============================
            split_chunks = splitter.split_text(
                content
            )

            for split_chunk in split_chunks:

                doc = Document(

                    page_content=split_chunk,

                    metadata={

                        "page":
                        chunk.get("page"),

                        "source":
                        chunk.get("source"),

                        "total_pages":
                        chunk.get("total_pages")
                    }
                )

                documents.append(doc)

        # =================================
        # STORE INTO CHROMA
        # =================================
        if documents:

            vector_db.add_documents(
                documents
            )

            vector_db.persist()

        return {
            "success": True,
            "stored_chunks":
            len(documents)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================
# SEARCH DOCUMENTS
# =========================================
def search_documents(
    query,
    top_k=5
):

    try:

        # =================================
        # SIMILARITY SEARCH WITH SCORE
        # =================================
        results = (
            vector_db.similarity_search_with_score(
                query,
                k=top_k
            )
        )

        formatted_results = []

        for doc, score in results:

            # lower score = better
            relevance = round(
                1 / (1 + score),
                3
            )

            # =============================
            # FILTER LOW RELEVANCE
            # =============================
            if relevance < 0.3:
                continue

            formatted_results.append({

                "content":
                doc.page_content,

                "page":
                doc.metadata.get(
                    "page",
                    "Unknown"
                ),

                "source":
                doc.metadata.get(
                    "source",
                    "Unknown"
                ),

                "total_pages":
                doc.metadata.get(
                    "total_pages",
                    "Unknown"
                ),

                "score":
                relevance
            })

        return formatted_results

    except Exception as e:

        return [{
            "error": str(e)
        }]