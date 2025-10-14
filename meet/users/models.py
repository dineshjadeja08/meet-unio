from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as the primary identifier."""
    
    OAUTH_CHOICES = [
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('none', 'None'),
    ]
    
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    oauth_provider = models.CharField(max_length=20, choices=OAUTH_CHOICES, default='none')
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
