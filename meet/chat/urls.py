from django.urls import path
from . import views

urlpatterns = [
    path('send', views.send_message, name='send_message'),
    path('messages/<int:meeting_id>', views.get_messages, name='get_messages'),
    path('file/upload', views.upload_file, name='upload_file'),
    path('file/download/<int:file_id>', views.download_file, name='download_file'),
]
