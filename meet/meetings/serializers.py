from rest_framework import serializers
from .models import Meeting, MeetingParticipant, MeetingInvite
from users.serializers import UserSerializer


class MeetingParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MeetingParticipant
        fields = ('id', 'user', 'joined_at', 'left_at')


class MeetingInviteSerializer(serializers.ModelSerializer):
    invitee = UserSerializer(read_only=True)
    
    class Meta:
        model = MeetingInvite
        fields = ('id', 'invitee', 'status', 'sent_at', 'responded_at')


class MeetingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    participants = MeetingParticipantSerializer(many=True, read_only=True)
    invites = MeetingInviteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meeting
        fields = ('id', 'meeting_id', 'title', 'description', 'host', 
                  'scheduled_at', 'duration', 'status', 'meeting_link',
                  'participants', 'invites', 'created_at', 'updated_at')
        read_only_fields = ('id', 'meeting_id', 'host', 'created_at', 'updated_at')


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('title', 'description', 'scheduled_at', 'duration')


class MeetingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('title', 'description', 'scheduled_at', 'duration', 'status')


class SendInviteSerializer(serializers.Serializer):
    meeting_id = serializers.IntegerField()
    invitee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
