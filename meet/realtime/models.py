from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class VideoCallSession(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('ringing', 'Ringing'),
        ('ongoing', 'Ongoing'),
        ('ended', 'Ended'),
        ('missed', 'Missed'),
    ]
    
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='call_sessions')
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in seconds')
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Call in {self.meeting.title} - {self.status}"
