from django.urls import path
from .views import homeowner_home_view , list_agents , send_connection_request , property_create

urlpatterns = [
    path('', homeowner_home_view, name='homeowner_home'),
    path('agents/', list_agents, name='list_agents'),
    path('send-connection-request/', send_connection_request, name='send_connection_request'),
    path('properties/create/', property_create, name='property_create'),
]
