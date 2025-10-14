from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os

User = get_user_model()


class ChatMessage(models.Model):
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.email}: {self.message[:30]}"


class SharedFile(models.Model):
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='shared_files')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(
        upload_to='meeting_files/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'zip']
            )
        ]
    )
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text='File size in bytes')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.meeting.title}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.filename = os.path.basename(self.file.name)
            self.file_size = self.file.size
        super().save(*args, **kwargs)
