from django.urls import path
from .views import homeowner_home_view , homeowner_invite_requests, send_connection_request , property_create

urlpatterns = [
    path('', homeowner_home_view, name='homeowner_home'),
    path('agents/', homeowner_invite_requests, name='homeowner_invite_requests'),
    path('send-connection-request/', send_connection_request, name='send_connection_request'),
    path('properties/create/', property_create, name='property_create'),
]
