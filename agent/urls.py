from django.urls import path
from .views import all_homeowners,homeowner_send_connection_request,dashboard_view, all_assistants , assistant_send_connection_request

urlpatterns = [
    # dashboard for agent and assistant
    path('agent-dashboard/', dashboard_view, name='dashboard'),
    # to see all homeowners
    path('all_homeowners/', all_homeowners, name='all_homeowners'),
    # to send invite to homeowners
    path('homeowner_send_connection_request/', homeowner_send_connection_request, name='homeowner_send_connection_request'),
    # to see all assistants
    path('all_assistants/', all_assistants, name='all_assistants'),
    # to send invite to assistants
    path('assistant_send_connection_request/', assistant_send_connection_request, name='assistant_send_connection_request'),
]
