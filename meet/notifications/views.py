from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer, SendNotificationSerializer
from meetings.models import Meeting

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    """
    Send push notifications for meeting invites or other purposes.
    """
    serializer = SendNotificationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    recipient_ids = serializer.validated_data['recipient_ids']
    title = serializer.validated_data['title']
    message = serializer.validated_data['message']
    notification_type = serializer.validated_data['notification_type']
    meeting_id = serializer.validated_data.get('meeting_id')
    
    related_meeting = None
    if meeting_id:
        related_meeting = get_object_or_404(Meeting, id=meeting_id)
    
    notifications_created = []
    errors = []
    
    for recipient_id in recipient_ids:
        try:
            recipient = User.objects.get(id=recipient_id)
            notification = Notification.objects.create(
                recipient=recipient,
                title=title,
                message=message,
                notification_type=notification_type,
                related_meeting=related_meeting
            )
            notifications_created.append(recipient.email)
        except User.DoesNotExist:
            errors.append(f'User with id {recipient_id} not found')
    
    return Response({
        'message': f'Notifications sent to {len(notifications_created)} users',
        'sent_to': notifications_created,
        'errors': errors
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """
    Fetch user notifications.
    """
    user = request.user
    
    # Filter parameters
    is_read = request.query_params.get('is_read')
    notification_type = request.query_params.get('type')
    
    notifications = Notification.objects.filter(recipient=user)
    
    if is_read is not None:
        is_read_bool = is_read.lower() == 'true'
        notifications = notifications.filter(is_read=is_read_bool)
    
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """
    Mark a notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Only recipient can mark as read
    if notification.recipient != request.user:
        return Response(
            {'error': 'You are not authorized to mark this notification as read.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()
    
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """
    Mark all notifications as read for the current user.
    """
    user = request.user
    updated = Notification.objects.filter(recipient=user, is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return Response({
        'message': f'{updated} notifications marked as read'
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """
    Delete a notification.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Only recipient can delete
    if notification.recipient != request.user:
        return Response(
            {'error': 'You are not authorized to delete this notification.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    notification.delete()
    return Response(
        {'message': 'Notification deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
    )
