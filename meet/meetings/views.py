from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from .models import Meeting, MeetingParticipant, MeetingInvite
from .serializers import (
    MeetingSerializer, MeetingCreateSerializer, MeetingUpdateSerializer,
    SendInviteSerializer
)

User = get_user_model()


class MeetingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for meeting management operations.
    """
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MeetingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MeetingUpdateSerializer
        return MeetingSerializer
    
    def get_queryset(self):
        """Filter meetings for the logged-in user."""
        # Handle schema generation (Swagger) when there's no real user
        if getattr(self, 'swagger_fake_view', False):
            return Meeting.objects.none()
        
        user = self.request.user
        # Get meetings where user is host or participant
        return Meeting.objects.filter(
            models.Q(host=user) | models.Q(participants__user=user)
        ).distinct()
    
    def list(self, request):
        """Get all meetings for the logged-in user."""
        queryset = self.get_queryset()
        serializer = MeetingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Get details of a specific meeting."""
        meeting = self.get_object()
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new meeting."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save(host=request.user)
            # Generate meeting link
            meeting.meeting_link = f"https://unio.app/meeting/{meeting.meeting_id}"
            meeting.save()
            
            return Response(
                MeetingSerializer(meeting).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Update meeting details."""
        meeting = self.get_object()
        
        # Only host can update meeting
        if meeting.host != request.user:
            return Response(
                {'error': 'Only the meeting host can update the meeting.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(MeetingSerializer(meeting).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Delete a meeting."""
        meeting = self.get_object()
        
        # Only host can delete meeting
        if meeting.host != request.user:
            return Response(
                {'error': 'Only the meeting host can delete the meeting.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        meeting.delete()
        return Response(
            {'message': 'Meeting deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get meeting history."""
        user = request.user
        meetings = Meeting.objects.filter(
            models.Q(host=user) | models.Q(participants__user=user),
            status='completed'
        ).distinct()
        
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a meeting."""
        meeting = self.get_object()
        
        # Only host can start meeting
        if meeting.host != request.user:
            return Response(
                {'error': 'Only the meeting host can start the meeting.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if meeting.status == 'ongoing':
            return Response(
                {'error': 'Meeting is already ongoing.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if meeting.status == 'completed':
            return Response(
                {'error': 'Meeting is already completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        meeting.status = 'ongoing'
        meeting.started_at = timezone.now()
        meeting.save()
        
        return Response({
            'message': 'Meeting started successfully',
            'meeting': MeetingSerializer(meeting).data
        })
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End a meeting."""
        meeting = self.get_object()
        
        # Only host can end meeting
        if meeting.host != request.user:
            return Response(
                {'error': 'Only the meeting host can end the meeting.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if meeting.status == 'completed':
            return Response(
                {'error': 'Meeting is already completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if meeting.status == 'scheduled':
            return Response(
                {'error': 'Cannot end a meeting that has not started yet.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        meeting.status = 'completed'
        meeting.ended_at = timezone.now()
        meeting.save()
        
        return Response({
            'message': 'Meeting ended successfully',
            'meeting': MeetingSerializer(meeting).data
        })
    
    @action(detail=True, methods=['post'])
    def send_invite(self, request, pk=None):
        """Send meeting invites to users."""
        meeting = self.get_object()
        
        # Only host can send invites
        if meeting.host != request.user:
            return Response(
                {'error': 'Only the meeting host can send invites.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        invitee_ids = request.data.get('invitee_ids', [])
        
        if not invitee_ids:
            return Response(
                {'error': 'invitee_ids is required and must not be empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invites_created = []
        errors = []
        
        for invitee_id in invitee_ids:
            try:
                invitee = User.objects.get(id=invitee_id)
                invite, created = MeetingInvite.objects.get_or_create(
                    meeting=meeting,
                    invitee=invitee
                )
                if created:
                    invites_created.append(invitee.email)
                else:
                    errors.append(f'{invitee.email} already invited')
            except User.DoesNotExist:
                errors.append(f'User with id {invitee_id} not found')
        
        return Response({
            'message': f'Invites sent to {len(invites_created)} users',
            'invited': invites_created,
            'errors': errors
        }, status=status.HTTP_201_CREATED)
