from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('meetings/<int:meeting_id>/messages/', views.get_messages, name='get_messages'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('meetings/<int:meeting_id>/files/', views.get_files, name='get_files'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
]
