from .rag import search_documents

def pdf_agent(query):

    context = search_documents(query)

    return context