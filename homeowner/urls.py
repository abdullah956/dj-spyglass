from django.urls import path
from .views import agent_invites_for_homeowner

urlpatterns = [
    # to see all agent invites for homeowner
    path('agent_invites_for_homeowner', agent_invites_for_homeowner, name='agent_invites_for_homeowner'),
]
