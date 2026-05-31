from django.urls import path

from api.views import (
    chat,
    upload_document,
    history,
    usage,
    health,
)

urlpatterns = [
    # ==========================
    # Chat APIs
    # ==========================
    path(
        "chat/",
        chat,
        name="chat"
    ),

    # ==========================
    # Document Upload APIs
    # ==========================
    path(
        "upload-document/",
        upload_document,
        name="upload_document"
    ),

    # ==========================
    # User Chat History
    # ==========================
    path(
        "history/",
        history,
        name="history"
    ),

    # ==========================
    # Usage / Billing
    # ==========================
    path(
        "usage/",
        usage,
        name="usage"
    ),

    # ==========================
    # Health Check
    # ==========================
    path(
        "health/",
        health,
        name="health"
    ),
]