from django.urls import path
from .views import agent_invites_for_homeowner , email_accept_connection_request

urlpatterns = [
    # to see all agent invites for homeowner
    path('agent_invites_for_homeowner', agent_invites_for_homeowner, name='agent_invites_for_homeowner'),
    # email 
    path('accept_connection_request/<int:request_id>/', email_accept_connection_request, name='accept_connection_request'),
]
