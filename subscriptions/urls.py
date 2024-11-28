from django.urls import path
from .views import subscription_page,payment_history,subscription_view ,subscribe_agent, subscribe_assistant ,subscription_success ,subscription_cancel
urlpatterns = [
    #path('',subscription_view, name='subscription'),
    # for assistant
    path('subscribe-assistant/<str:subscription_type>/', subscribe_assistant, name='subscribe_assistant'),
    # for agent
    path('subscribe-agent/<str:subscription_type>/', subscribe_agent, name='subscribe_agent'),
    # for success
    path('subscription-success/<int:subscription_id>/', subscription_success, name='subscription_success'),
    # for cancel
    path('subscription-cancel/', subscription_cancel, name='subscription_cancel'),
    # for history
    path('payment-history/', payment_history, name='payment_history'),
    # subs
    path('subscription/', subscription_page, name='subscription_page'),
]