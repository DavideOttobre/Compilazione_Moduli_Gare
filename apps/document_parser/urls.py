# Story 2.1: Upload File PDF e DOCX
# URL routing per document_parser app
# CR Fix #4: Removed Story 2.2 scope creep (parse/ URL)

from django.urls import path
from . import views

app_name = 'document_parser'

urlpatterns = [
    # AC-1: Path documents/upload/
    path('upload/', views.upload_document, name='upload_document'),
    # AC-2: Path documents/upload/success/<pk>/
    path('upload/success/<int:pk>/', views.upload_success, name='upload_success'),
    # Story 2.4: Path documents/parse-docx/<pk>/
    path('parse-docx/<int:pk>/', views.parse_docx_document, name='parse_docx_document'),
]
