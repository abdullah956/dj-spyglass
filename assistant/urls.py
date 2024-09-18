from django.urls import path
from .views import asssistant_invite_requests,send_connection_request, homeowner_connection_requests_all_agents
urlpatterns = [
    path('agents/', asssistant_invite_requests, name='asssistant_invite_requests'),

    path('send-connection-request/', send_connection_request, name='assistant_send_connection_request'),

    path('homeowner_connection_requests_all_agents/', homeowner_connection_requests_all_agents, name='homeowner_connection_requests_all_agents'),
]
