from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="legal_db",
    embedding_function=embedding
)

def store_document(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    vector_db.add_texts(chunks)

    vector_db.persist()

def search_documents(query):

    docs = vector_db.similarity_search(query, k=4)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"

    return context