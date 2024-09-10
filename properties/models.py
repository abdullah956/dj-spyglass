from django.db import models
from config.models import BasedModel
from agent.models import Agent
from homeowner.models import Homeowner
from django.db import models

class Property(BasedModel):
    PROCESS_CHOICES = [
        ('%', 'Percentage'),
        ('&', 'And'),
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
    compensation = models.DecimalField(max_digits=10, decimal_places=2)
    square_feet = models.IntegerField()
    contract = models.FileField(upload_to='contracts/', blank=True, null=True)
    property_images = models.ImageField(upload_to='property_images/', blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)  
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Property at {self.address} - {self.state}"

