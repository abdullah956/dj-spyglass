from django.urls import path
from .views import subscription_view ,subscribe_agent, subscribe_assistant ,subscription_success ,subscription_cancel
urlpatterns = [
    #path('',subscription_view, name='subscription'),
    # intialize subcription
    path('subscribe-assistant/<str:subscription_type>/', subscribe_assistant, name='subscribe_assistant'),

    path('subscribe-agent/<str:subscription_type>/', subscribe_agent, name='subscribe_agent'),
    path('subscription-success/<int:subscription_id>/', subscription_success, name='subscription_success'),
    path('subscription-cancel/', subscription_cancel, name='subscription_cancel'),
]