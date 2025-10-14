from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.MeetingViewSet, basename='meeting')

urlpatterns = [
    path('invite', views.send_invite, name='send_invite'),
    path('', include(router.urls)),
]
