from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_email = serializers.EmailField(source='recipient.email', read_only=True)
    meeting_title = serializers.CharField(source='related_meeting.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'recipient_email', 'title', 'message', 
                  'notification_type', 'is_read', 'related_meeting', 'meeting_title',
                  'created_at', 'read_at')
        read_only_fields = ('id', 'recipient', 'created_at', 'read_at')


class SendNotificationSerializer(serializers.Serializer):
    recipient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(
        choices=Notification.NOTIFICATION_TYPES,
        default='general'
    )
    meeting_id = serializers.IntegerField(required=False, allow_null=True)
