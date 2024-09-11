from django.urls import path
from .views import homeowner_home_view , list_agents 

urlpatterns = [
    path('', homeowner_home_view, name='homeowner_home'),
    path('agents/', list_agents, name='list_agents'),
]
