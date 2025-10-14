from django.contrib import admin
from .models import VideoCallSession


@admin.register(VideoCallSession)
class VideoCallSessionAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'caller', 'receiver', 'status', 'started_at', 'ended_at')
    list_filter = ('status', 'started_at')
    search_fields = ('meeting__title', 'caller__email', 'receiver__email')
