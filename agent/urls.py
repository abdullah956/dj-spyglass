from django.urls import path
from .views import all_homeowners,homeowner_requests_status_by_agent,homeowner_send_connection_request,dashboard_view, all_assistants , assistant_send_connection_request

urlpatterns = [
    # dashboard for agent and assistant
    path('agent-dashboard/', dashboard_view, name='dashboard'),
    # to see all homeowners
    path('all-homeowners/', all_homeowners, name='all_homeowners'),
    # to send invite to homeowners
    path('homeowner-send-connection-request/', homeowner_send_connection_request, name='homeowner_send_connection_request'),
    # to see all assistants
    path('all-assistants/', all_assistants, name='all_assistants'),
    # to send invite to assistants
    path('assistant-send-connection-request/', assistant_send_connection_request, name='assistant_send_connection_request'),
    # to see the status of request of homeowners
    path('homeowner-requests-status-by-agent/', homeowner_requests_status_by_agent, name='homeowner_requests_status_by_agent'),
]
