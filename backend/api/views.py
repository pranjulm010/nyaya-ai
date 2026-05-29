from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .pdf import extract_pdf_text
from .rag import store_document

from .router_agent import router_agent
from .memory_agent import save_memory

@api_view(["POST"])
def upload_pdf(request):

    pdf_file = request.FILES.get("file")

    text = extract_pdf_text(pdf_file)

    store_document(text)

    return Response({
        "message": "PDF uploaded"
    })

@api_view(["POST"])
def chat(request):

    query = request.data.get("query")

    save_memory("user", query)

    answer = router_agent(query)

    save_memory("assistant", answer)

    return Response({
        "answer": answer
    })