from django.contrib import admin
from .models import Meeting, MeetingParticipant, MeetingInvite


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'scheduled_at', 'status', 'created_at')
    list_filter = ('status', 'scheduled_at', 'created_at')
    search_fields = ('title', 'host__email', 'meeting_id')
    ordering = ('-created_at',)


@admin.register(MeetingParticipant)
class MeetingParticipantAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'user', 'joined_at', 'left_at')
    list_filter = ('joined_at',)
    search_fields = ('meeting__title', 'user__email')


@admin.register(MeetingInvite)
class MeetingInviteAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'invitee', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('meeting__title', 'invitee__email')
