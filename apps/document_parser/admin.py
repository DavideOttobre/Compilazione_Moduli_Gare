from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'file_type', 'file_size', 'user', 'status', 'uploaded_at')
    list_filter = ('file_type', 'status', 'uploaded_at')
    search_fields = ('original_name',)
    readonly_fields = ('uploaded_at',)
