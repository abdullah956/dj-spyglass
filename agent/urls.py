from django.urls import path
from .views import all_homeowners,homeowner_send_connection_request,dashboard_view

urlpatterns = [
    # dashboard for agent and assistant
    path('agent-dashboard/', dashboard_view, name='dashboard'),
    # to see all homeowners
    path('all_homeowners/', all_homeowners, name='all_homeowners'),
    # to send invite to all homeowners
    path('homeowner_send_connection_request/', homeowner_send_connection_request, name='homeowner_send_connection_request'),
]
