from django.urls import path
from .views import assistant_home_view, asssistant_invite_requests,send_connection_request
urlpatterns = [
    path('', assistant_home_view, name='assistant_home'),
    path('agents/', asssistant_invite_requests, name='asssistant_invite_requests'),
    path('send-connection-request/', send_connection_request, name='assistant_send_connection_request'),
]
