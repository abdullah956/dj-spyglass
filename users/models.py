from django.db import models
from django.contrib.auth.models import AbstractUser
from config.models import BasedModel
from .managers import UserManager
from django.conf import settings

class User(AbstractUser, BasedModel):
    ROLE_CHOICES = [
        ('SuperAdmin', 'SuperAdmin'),
        ('SubAdmin', 'SubAdmin'),
        ('Agent', 'Agent'),
        ('Homeowner', 'Homeowner'),
        ('Assistant', 'Assistant'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email


class Agent(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    assistant = models.ForeignKey('Assistant', on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    homeowners_json = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Agent: {self.user.email}"

class Homeowner(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homeowner_profile')

    def __str__(self):
        return f"Homeowner: {self.user.email}"

class Assistant(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assistant_profile')

    def __str__(self):
        return f"Assistant: {self.user.email}"

class Contact(BasedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    
    def __str__(self):
        return f'{self.name} - {self.email}'

class NewsletterSubscription(BasedModel):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} (Subscribed on: {self.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')})"
    
    