from rest_framework import serializers
from .models import VideoCallSession


class VideoCallSessionSerializer(serializers.ModelSerializer):
    caller_email = serializers.EmailField(source='caller.email', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)
    
    class Meta:
        model = VideoCallSession
        fields = ('id', 'meeting', 'caller', 'caller_email', 'receiver', 
                  'receiver_email', 'status', 'started_at', 'ended_at', 'duration')
        read_only_fields = ('id', 'started_at', 'duration')
