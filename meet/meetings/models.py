from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Meeting(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    meeting_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')
    scheduled_at = models.DateTimeField()
    duration = models.IntegerField(help_text='Duration in minutes', default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"{self.title} - {self.host.email}"


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('meeting', 'user')
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.email} in {self.meeting.title}"


class MeetingInvite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='invites')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_invites')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('meeting', 'invitee')
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Invite to {self.invitee.email} for {self.meeting.title}"
