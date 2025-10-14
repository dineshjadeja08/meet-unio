from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('call/start', views.start_call, name='start_call'),
    path('call/end', views.end_call, name='end_call'),
]
