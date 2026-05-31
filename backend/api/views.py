import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from agents.router_agent import router_agent

from rag.document_extractor import extract_document_text
from rag.vector_store import store_document_chunks

from memory.memory_service import get_chat_history
from billing.usage_tracker import get_usage_summary

from core.logger import log_error


@api_view(["POST"])
def chat(request):
    """
    POST /api/chat/

    Body:
    {
        "query": "What is Article 21?",
        "user_id": "user123",
        "session_id": "optional",
        "user_type": "public/lawyer",
        "document_id": "optional"
    }
    """

    try:
        query = request.data.get(
            "query",
            ""
        ).strip()

        if not query:
            return Response(
                {
                    "success": False,
                    "message": "Query is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = request.data.get(
            "user_id",
            "anonymous"
        )

        session_id = request.data.get(
            "session_id"
        ) or str(uuid.uuid4())

        user_type = request.data.get(
            "user_type",
            "public"
        )

        document_id = request.data.get(
            "document_id"
        )

        result = router_agent(
            query=query,
            user_id=user_id,
            session_id=session_id,
            user_type=user_type,
            document_id=document_id,
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    except Exception as error:
        log_error(
            module="api.views.chat",
            message="Chat API failed",
            error=str(error)
        )

        return Response(
            {
                "success": False,
                "message": "Chat processing failed.",
                "error": str(error)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def upload_document(request):
    """
    POST /api/upload-document/

    form-data:
    file: document
    user_id: user123
    """

    try:
        uploaded_file = request.FILES.get(
            "file"
        )

        if not uploaded_file:
            return Response(
                {
                    "success": False,
                    "message": "No document uploaded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        supported_extensions = [
            ".pdf",
            ".docx",
            ".txt",
            ".md",
        ]

        is_supported = any(
            uploaded_file.name.lower().endswith(ext)
            for ext in supported_extensions
        )

        if not is_supported:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Unsupported file type. "
                        "Supported: PDF, DOCX, TXT, MD"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_id = request.data.get(
            "user_id",
            "anonymous"
        )

        document_id = str(uuid.uuid4())

        storage = FileSystemStorage(
            location=getattr(
                settings,
                "DOCUMENT_UPLOAD_DIR",
                "storage/uploaded_pdfs"
            )
        )

        saved_filename = storage.save(
            f"{document_id}_{uploaded_file.name}",
            uploaded_file
        )

        saved_path = storage.path(
            saved_filename
        )

        extraction_result = extract_document_text(
            file_path=saved_path,
            user_id=user_id,
            document_id=document_id,
            source_name=uploaded_file.name,
        )

        if not extraction_result.get(
            "success"
        ):
            return Response(
                {
                    "success": False,
                    "message": "Document extraction failed.",
                    "error": extraction_result.get(
                        "error"
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        store_result = store_document_chunks(
            chunks=extraction_result.get(
                "chunks",
                []
            ),
            user_id=user_id,
            document_id=document_id,
        )

        if not store_result.get(
            "success"
        ):
            return Response(
                {
                    "success": False,
                    "message": "Document indexing failed.",
                    "error": store_result.get(
                        "error"
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "message": (
                    "Document uploaded "
                    "and indexed successfully."
                ),
                "user_id": user_id,
                "document_id": document_id,
                "file_name": uploaded_file.name,
                "stored_file": saved_filename,
                "document_type":
                extraction_result.get(
                    "document_type"
                ),
                "total_pages":
                extraction_result.get(
                    "total_pages"
                ),
                "total_chunks":
                len(
                    extraction_result.get(
                        "chunks",
                        []
                    )
                ),
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as error:
        log_error(
            module="api.views.upload_document",
            message="Document upload failed",
            error=str(error)
        )

        return Response(
            {
                "success": False,
                "message": "Document upload failed.",
                "error": str(error)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def history(request):
    """
    GET /api/history/

    Query Params:
    ?user_id=123
    &session_id=abc
    """

    try:
        user_id = request.GET.get(
            "user_id",
            "anonymous"
        )

        session_id = request.GET.get(
            "session_id",
            "default"
        )

        messages = get_chat_history(
            user_id=user_id,
            session_id=session_id
        )

        return Response(
            {
                "success": True,
                "user_id": user_id,
                "session_id": session_id,
                "history": messages,
            },
            status=status.HTTP_200_OK
        )

    except Exception as error:
        return Response(
            {
                "success": False,
                "message": (
                    "Failed to fetch history."
                ),
                "error": str(error)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def usage(request):
    """
    GET /api/usage/

    Query Params:
    ?user_id=123
    """

    try:
        user_id = request.GET.get(
            "user_id",
            "anonymous"
        )

        usage_data = get_usage_summary(
            user_id=user_id
        )

        return Response(
            {
                "success": True,
                "user_id": user_id,
                "usage": usage_data,
            },
            status=status.HTTP_200_OK
        )

    except Exception as error:
        return Response(
            {
                "success": False,
                "message": (
                    "Failed to fetch usage."
                ),
                "error": str(error)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def health(request):
    """
    GET /api/health/
    """

    return Response(
        {
            "success": True,
            "status": "ok",
            "service": "Nyaya AI Backend",
        },
        status=status.HTTP_200_OK
    )