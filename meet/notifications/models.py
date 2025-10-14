from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('meeting_invite', 'Meeting Invite'),
        ('meeting_reminder', 'Meeting Reminder'),
        ('meeting_started', 'Meeting Started'),
        ('meeting_cancelled', 'Meeting Cancelled'),
        ('message', 'Message'),
        ('general', 'General'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    related_meeting = models.ForeignKey(
        'meetings.Meeting', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.email}"
