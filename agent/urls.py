from django.urls import path
from .views import agent_dashboard_view,assistant_update_request_status,agent_home_view,connection_requests_view,update_request_status,property_approval_list,property_approve, assistant_connection_requests_view

urlpatterns = [
    path('', agent_home_view, name='agent_home'),
    path('requests/', connection_requests_view, name='connection_requests'),
    path('requests/update/<int:request_id>/', update_request_status, name='update_request_status'),
    path('properties/approval/', property_approval_list, name='property_approval_list'),
    path('properties/approve/<int:property_id>/', property_approve, name='property_approve'),
    path('assistant-requests/', assistant_connection_requests_view, name='assistant_connection_requests'),
    path('assistant-requests/update/<int:request_id>/', assistant_update_request_status, name='assistant_update_request_status'),
    path('agent-dashboard/', agent_dashboard_view, name='agent_dashboard'),
]
