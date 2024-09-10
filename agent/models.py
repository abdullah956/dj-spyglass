from django.db import models
from config import settings
from config.models import BasedModel
from django.contrib.auth.models import User

class Agent(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correct reference to custom User model
    assistants = models.ManyToManyField('assistant.Assistant', related_name='assigned_agents', blank=True)  # Unique related_name

    def __str__(self):
        return f"Agent: {self.user.email}"
