from django.urls import path
from .views import agents_invites, agent_update_request_status

urlpatterns = [
    # to see all agent 
    path('agents-invites', agents_invites, name='agent_invites'),
    # to update all agent requests
    path('agent-update-request-status/', agent_update_request_status, name='agent_update_request_status'),
]
