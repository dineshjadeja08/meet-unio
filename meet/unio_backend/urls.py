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
        1. Login via `/api/auth/login` to get your JWT token
        2. Click the "Authorize" button (🔓) at the top right
        3. Enter: `Bearer <your_access_token>` (include the word "Bearer" followed by a space)
        4. Click "Authorize" then "Close"
        
        All authenticated endpoints will now work with your token.
        """,
        terms_of_service="https://www.unio.com/terms/",
        contact=openapi.Contact(email="support@unio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
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
