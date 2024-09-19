from django.urls import path
from .views import agents_invites

urlpatterns = [
    # to see all agent 
    path('agents-invites', agents_invites, name='agent_invites'),
]
