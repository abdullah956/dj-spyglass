from django.db import models
from config.models import BasedModel
from config import settings


class Assistant(BasedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agents = models.ManyToManyField('agent.Agent', related_name='assigned_assistants', blank=True)  # Unique related_name

    def __str__(self):
        return f"Assistant: {self.user.email}"