from django.db import models
from users.models import User
from datetime import timedelta
from django.utils import timezone
from config.models import BasedModel

class Subscription(BasedModel):
    SUBSCRIPTION_TYPES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    payment_successful = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.subscription_type == 'monthly':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == 'yearly':
                self.end_date = self.start_date + timedelta(days=365)
        self.check_subscription_status()
        super().save(*args, **kwargs)
    def check_subscription_status(self):
        if timezone.now() > self.end_date:
            self.is_active = False
    def __str__(self):
        return f"{self.user.email} - {self.subscription_type}"