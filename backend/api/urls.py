from django.urls import path
from .views import upload_pdf, chat

urlpatterns = [
    path("upload/", upload_pdf),
    path("chat/", chat),
]