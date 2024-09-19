from django.urls import path
from .views import agent_invites_for_assistant,all_homeowners_for_assistant,assistant_send_connection_request_homeowner

urlpatterns = [
    # to see all agent invites for assistant
    path('agent-invites-for-assistant', agent_invites_for_assistant, name='agent_invites_for_assistant'),
    # to see all homeowners for the agent
    path('all_homeowners_for_assistant', all_homeowners_for_assistant, name='all_homeowners_for_assistant'),
    # send connection requests to homeowenrs by the assistant
    path('assistant_send_connection_request_homeowner',assistant_send_connection_request_homeowner , name='assistant_send_connection_request_homeowner'),
]




