from django.urls import path
from .views import homeowner_invite_requests, homeownersend_connection_request , property_create

urlpatterns = [
    path('agents/', homeowner_invite_requests, name='homeowner_invite_requests'),
    path('send-connection-request/', homeownersend_connection_request, name='homeowner_send_connection_request'),
    path('properties/create/', property_create, name='property_create'),
]
