from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.conf import settings
from .models import ChatMessage, SharedFile
from .serializers import (
    ChatMessageSerializer, SendMessageSerializer,
    SharedFileSerializer, FileUploadSerializer
)
from meetings.models import Meeting
import os


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a message in a meeting.
    """
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    meeting_id = serializer.validated_data['meeting_id']
    message_text = serializer.validated_data['message']
    
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Create message
    message = ChatMessage.objects.create(
        meeting=meeting,
        sender=request.user,
        message=message_text
    )
    
    response_serializer = ChatMessageSerializer(message)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, meeting_id):
    """
    Fetch all messages for a meeting.
    """
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Check if user is part of the meeting
    is_host = meeting.host == request.user
    is_participant = meeting.participants.filter(user=request.user).exists()
    
    if not (is_host or is_participant):
        return Response(
            {'error': 'You are not authorized to view messages in this meeting.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    messages = ChatMessage.objects.filter(meeting=meeting)
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Upload a file during a meeting.
    """
    serializer = FileUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    meeting_id = serializer.validated_data['meeting_id']
    uploaded_file = serializer.validated_data['file']
    
    # Check file size
    if uploaded_file.size > settings.MAX_UPLOAD_SIZE:
        return Response(
            {'error': f'File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / 1048576}MB'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check file extension
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        return Response(
            {'error': f'File type {file_ext} is not allowed. Allowed types: {", ".join(settings.ALLOWED_UPLOAD_EXTENSIONS)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Create shared file
    shared_file = SharedFile.objects.create(
        meeting=meeting,
        uploaded_by=request.user,
        file=uploaded_file
    )
    
    response_serializer = SharedFileSerializer(shared_file, context={'request': request})
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    """
    Download a shared file.
    """
    shared_file = get_object_or_404(SharedFile, id=file_id)
    
    # Check if user is part of the meeting
    meeting = shared_file.meeting
    is_host = meeting.host == request.user
    is_participant = meeting.participants.filter(user=request.user).exists()
    
    if not (is_host or is_participant):
        return Response(
            {'error': 'You are not authorized to download this file.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        file_path = shared_file.file.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{shared_file.filename}"'
            return response
        else:
            raise Http404('File not found')
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
