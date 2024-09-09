from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from config.models import BasedModel
from .managers import UserManager

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
    subscription_status = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        # Set related_name to avoid clashes
        permissions = [('can_change_password', 'Can change password')]

    # Ensure that reverse accessor names don't clash
    groups = models.ManyToManyField(
        Group,
        related_name='%(app_label)s_%(class)s',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='%(app_label)s_%(class)s',
        blank=True,
    )