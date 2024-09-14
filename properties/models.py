from django.db import models
from config import settings
from config.models import BasedModel
from django.db import models
from users.models import Agent , Homeowner , Assistant

from django.db import models

class Property(BasedModel):
    PROCESS_CHOICES = [
        ('%', 'Percentage'),
        ('$', 'Dollar'),
        ('Contact Agent', 'Contact Agent'),
        ('Send Offer', 'Send Offer'),
    ]

    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    agent_remarks = models.TextField(blank=True, null=True)
    process = models.CharField(max_length=15, choices=PROCESS_CHOICES)
    compensation = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    square_feet = models.IntegerField()
    document = models.FileField(upload_to='document/', blank=True, null=True)
    contract = models.FileField(upload_to='contracts/', blank=True, null=True)
    property_images = models.ImageField(upload_to='property_images/', blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE,blank=True, null=True)
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE, blank=True, null=True)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, blank=True, null=True)
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Property at {self.address} - {self.state}"

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE ,blank=True, null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE ,blank=True, null=True)
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Request from {self.sender} to {self.receiver} ({self.get_status_display()})"