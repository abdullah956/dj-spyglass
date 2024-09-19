from django.urls import path
from .views import agent_invites_for_assistant

urlpatterns = [
    # to see all agent invites for assistant
    path('agent-invites-for-assistant', agent_invites_for_assistant, name='agent_invites_for_assistant'),
]




