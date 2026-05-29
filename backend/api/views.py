import uuid

from django.shortcuts import render

from rest_framework.decorators import (
    api_view
)

from rest_framework.response import (
    Response
)

from rest_framework import status


# =========================================
# IMPORT SERVICES
# =========================================
from .pdf import extract_pdf_text

from .rag import store_document

from .router_agent import (
    router_agent
)

from .memory_agent import (
    save_memory
)


# =========================================
# PDF UPLOAD API
# =========================================
@api_view(["POST"])
def upload_pdf(request):

    try:

        # =================================
        # GET FILE
        # =================================
        pdf_file = request.FILES.get(
            "file"
        )

        if not pdf_file:

            return Response(
                {
                    "success": False,
                    "message":
                    "No PDF file uploaded."
                },
                status=400
            )

        # =================================
        # EXTRACT PDF TEXT
        # =================================
        pdf_data = extract_pdf_text(
            pdf_file
        )

        if not pdf_data["success"]:

            return Response(
                {
                    "success": False,
                    "message":
                    "PDF extraction failed.",
                    "error":
                    pdf_data["error"]
                },
                status=500
            )

        # =================================
        # STORE INTO VECTOR DB
        # =================================
        store_result = store_document(
            pdf_data
        )

        if not store_result["success"]:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to store document.",
                    "error":
                    store_result["error"]
                },
                status=500
            )

        # =================================
        # SUCCESS RESPONSE
        # =================================
        return Response({

            "success": True,

            "message":
            "PDF uploaded successfully.",

            "total_chunks":
            store_result[
                "stored_chunks"
            ],

            "total_pages":
            pdf_data[
                "total_pages"
            ],

            "file_name":
            pdf_file.name
        })

    except Exception as e:

        return Response({

            "success": False,

            "message":
            "Unexpected error occurred.",

            "error": str(e)

        }, status=500)


# =========================================
# CHAT API
# =========================================
@api_view(["POST"])
def chat(request):

    try:

        # =================================
        # GET QUERY
        # =================================
        query = request.data.get(
            "query",
            ""
        ).strip()

        if not query:

            return Response({

                "success": False,

                "message":
                "Query is required."

            }, status=400)

        # =================================
        # SESSION HANDLING
        # =================================
        session_id = request.data.get(
            "session_id"
        )

        if not session_id:

            session_id = str(
                uuid.uuid4()
            )

        # =================================
        # USER HANDLING
        # =================================
        user_id = request.data.get(
            "user_id",
            "anonymous"
        )

        # =================================
        # SAVE USER MEMORY
        # =================================
        save_memory(

            role="user",

            content=query,

            session_id=session_id,

            user_id=user_id
        )

        # =================================
        # ROUTER AGENT
        # =================================
        answer = router_agent(
            user_query=query
        )

        # =================================
        # SAVE ASSISTANT MEMORY
        # =================================
        save_memory(

            role="assistant",

            content=answer,

            session_id=session_id,

            user_id=user_id
        )

        # =================================
        # FINAL RESPONSE
        # =================================
        return Response({

            "success": True,

            "session_id":
            session_id,

            "query":
            query,

            "answer":
            answer
        })

    except Exception as e:

        return Response({

            "success": False,

            "message":
            "Chat processing failed.",

            "error":
            str(e)

        }, status=500)