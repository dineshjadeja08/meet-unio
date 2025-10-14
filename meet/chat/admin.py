from django.contrib import admin
from .models import ChatMessage, SharedFile


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'meeting', 'message_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__email', 'meeting__title', 'message')
    ordering = ('-created_at',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_by', 'meeting', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'uploaded_by__email', 'meeting__title')
    ordering = ('-uploaded_at',)
