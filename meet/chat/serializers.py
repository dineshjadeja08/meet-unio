from rest_framework import serializers
from .models import ChatMessage, SharedFile
from users.serializers import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ('id', 'meeting', 'sender', 'sender_email', 'message', 'created_at')
        read_only_fields = ('id', 'sender', 'created_at')


class SendMessageSerializer(serializers.Serializer):
    meeting_id = serializers.IntegerField()
    message = serializers.CharField(max_length=5000)


class SharedFileSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SharedFile
        fields = ('id', 'meeting', 'uploaded_by', 'uploaded_by_email', 
                  'file', 'file_url', 'filename', 'file_size', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_by', 'filename', 'file_size', 'uploaded_at')
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class FileUploadSerializer(serializers.Serializer):
    meeting_id = serializers.IntegerField()
    file = serializers.FileField()
