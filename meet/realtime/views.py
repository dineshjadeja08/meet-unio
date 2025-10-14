from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import VideoCallSession
from .serializers import VideoCallSessionSerializer
from meetings.models import Meeting


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_call(request):
    """
    Start a video call session.
    """
    meeting_id = request.data.get('meeting_id')
    receiver_id = request.data.get('receiver_id')
    
    if not meeting_id:
        return Response(
            {'error': 'meeting_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Create call session
    call_session = VideoCallSession.objects.create(
        meeting=meeting,
        caller=request.user,
        receiver_id=receiver_id if receiver_id else None,
        status='initiated'
    )
    
    # Update meeting status
    meeting.status = 'ongoing'
    meeting.save()
    
    serializer = VideoCallSessionSerializer(call_session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_call(request):
    """
    End a video call session.
    """
    call_id = request.data.get('call_id')
    
    if not call_id:
        return Response(
            {'error': 'call_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    call_session = get_object_or_404(VideoCallSession, id=call_id)
    
    # Only caller or receiver can end the call
    if request.user not in [call_session.caller, call_session.receiver]:
        return Response(
            {'error': 'You are not authorized to end this call'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # End the call
    call_session.status = 'ended'
    call_session.ended_at = timezone.now()
    
    # Calculate duration
    if call_session.started_at:
        duration = (call_session.ended_at - call_session.started_at).total_seconds()
        call_session.duration = int(duration)
    
    call_session.save()
    
    # Update meeting status
    meeting = call_session.meeting
    meeting.status = 'completed'
    meeting.save()
    
    serializer = VideoCallSessionSerializer(call_session)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Check backend server health.
    """
    return Response({
        'status': 'healthy',
        'message': 'UNIO Backend API is running',
        'timestamp': timezone.now()
    }, status=status.HTTP_200_OK)
