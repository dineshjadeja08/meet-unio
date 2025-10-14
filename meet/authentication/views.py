from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

from .serializers import UserRegistrationSerializer, UserLoginSerializer, OAuthSerializer

User = get_user_model()


@swagger_auto_schema(
    method='post',
    operation_description="Register a new user account with email and password",
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            examples={
                "application/json": {
                    "message": "User created successfully",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "johndoe",
                        "first_name": "John",
                        "last_name": "Doe"
                    },
                    "tokens": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                    }
                }
            }
        ),
        400: "Bad Request - Validation errors"
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Create a new user account.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Authenticate user with email and password, returns JWT tokens",
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "message": "Login successful",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "johndoe"
                    },
                    "tokens": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                    }
                }
            }
        ),
        401: "Unauthorized - Invalid credentials"
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user and return JWT token.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout user and invalidate refresh token.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_oauth(request):
    """
    Login using Google OAuth2.0.
    """
    serializer = OAuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    token = serializer.validated_data['access_token']
    
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            settings.GOOGLE_OAUTH2_CLIENT_ID
        )
        
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': first_name,
                'last_name': last_name,
                'oauth_provider': 'google'
            }
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Google login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def microsoft_oauth(request):
    """
    Login using Microsoft OAuth2.0.
    """
    serializer = OAuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    token = serializer.validated_data['access_token']
    
    try:
        # Verify token with Microsoft Graph API
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        
        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = response.json()
        email = user_info.get('mail') or user_info.get('userPrincipalName')
        first_name = user_info.get('givenName', '')
        last_name = user_info.get('surname', '')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': first_name,
                'last_name': last_name,
                'oauth_provider': 'microsoft'
            }
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Microsoft login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
