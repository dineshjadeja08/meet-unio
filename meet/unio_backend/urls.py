"""
URL configuration for unio_backend project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="UNIO Backend API",
        default_version='v1',
        description="""
        Complete API documentation for UNIO video conferencing backend.
        
        ## Features
        - **Authentication**: JWT & OAuth (Google, Microsoft)
        - **User Management**: CRUD operations with permissions
        - **Meeting Management**: Create, schedule, and manage meetings
        - **Real-Time Communication**: WebSocket for WebRTC signaling
        - **Chat & File Sharing**: In-meeting chat and file uploads
        - **Notifications**: Push notifications for meeting events
        
        ## Authentication
        Most endpoints require JWT authentication. Use the `/api/auth/login` endpoint to obtain a token,
        then include it in the Authorization header: `Bearer <your_token>`
        """,
        terms_of_service="https://www.unio.com/terms/",
        contact=openapi.Contact(email="support@unio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
    path('api/meetings/', include('meetings.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/health/', include('realtime.urls')),
    
    # Swagger UI documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),  # Root redirects to Swagger
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
