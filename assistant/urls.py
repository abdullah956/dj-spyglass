from django.urls import path
from .views import assistant_home_view, agent_list,send_connection_request
urlpatterns = [
    path('', assistant_home_view, name='assistant_home'),
    path('agents/', agent_list, name='agents_list'),
    path('send-connection-request/', send_connection_request, name='assistant_send_connection_request'),
    #path('assistant-dashboard/', assistant_dashboard_view, name='assistant_dashboard'),
]
