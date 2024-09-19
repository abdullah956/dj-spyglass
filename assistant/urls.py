from django.urls import path
from .views import agent_invites_for_assistant,assistant_send_connection_request_homeowner,homeowner_requests_status_by_assistant

urlpatterns = [
    # to see all agent invites for assistant
    path('agent-invites-for-assistant/', agent_invites_for_assistant, name='agent_invites_for_assistant'),
    # to see all homeowners for the agent
    #path('all-homeowners-for-assistant/', all_homeowners_for_assistant, name='all_homeowners_for_assistant'),
    # send connection requests to homeowenrs by the assistant
    path('assistant-send-connection-request-homeowner/',assistant_send_connection_request_homeowner , name='assistant_send_connection_request_homeowner'),
    # homeowner request status assistant pov
    path('homeowner-requests-status-by-assistant', homeowner_requests_status_by_assistant, name='homeowner_requests_status_by_assistant'),
]




