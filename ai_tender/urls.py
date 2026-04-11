"""
URL configuration for ai_tender project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    # Story 2.1: Include document_parser URLs
    path('documents/', include('apps.document_parser.urls')),
]
