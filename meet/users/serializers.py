from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                  'profile_picture', 'oauth_provider', 'date_joined', 'is_active')
        read_only_fields = ('id', 'date_joined', 'oauth_provider')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_picture')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
