from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def list(self, request):
        """Get a list of all users (admin only)."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Get details of a user by ID."""
        user = self.get_object()
        
        # Non-admin users can only view their own profile
        if not request.user.is_staff and request.user.id != user.id:
            return Response(
                {'error': 'You do not have permission to view this user.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new user (admin use)."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Update user profile details."""
        user = self.get_object()
        
        # Non-admin users can only update their own profile
        if not request.user.is_staff and request.user.id != user.id:
            return Response(
                {'error': 'You do not have permission to update this user.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Delete a user (admin use)."""
        user = self.get_object()
        user.delete()
        return Response(
            {'message': 'User deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
