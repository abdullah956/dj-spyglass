from django.db import models
from django.contrib.auth.models import User
from config import settings
from config.models import BasedModel

class Homeowner(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent = models.ForeignKey('agent.Agent', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Homeowner: {self.user.email}"
