from django.urls import path
from .views import agent_home_view,connection_requests_view,update_request_status

urlpatterns = [
    path('', agent_home_view, name='agent_home'),
    path('requests/', connection_requests_view, name='connection_requests'),
    path('requests/update/<int:request_id>/', update_request_status, name='update_request_status'),
]
