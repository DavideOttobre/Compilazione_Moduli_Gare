# Story 2.1/2.2: Upload e Parsing PDF
# URL routing per document_parser app

from django.urls import path
from . import views

app_name = 'document_parser'

urlpatterns = [
    # AC-1: Path documents/upload/
    path('upload/', views.upload_document, name='upload_document'),
    # AC-2: Path documents/upload/success/<pk>/
    path('upload/success/<int:pk>/', views.upload_success, name='upload_success'),
    # Story 2.2: Parsing PDF nativo
    path('parse/<int:pk>/', views.parse_document, name='parse_document'),
]
