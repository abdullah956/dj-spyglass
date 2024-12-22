from django.urls import path
from .views import signup_by_invite,send_connection_request_by_form,searched,all_agent_properties_dashboard,agent_profile_by_ID,agent_profile,assistant_profile,homeowner_profile,all_homeowners,assistant_requests_status_by_agent,homeowner_requests_status_by_agent,homeowner_send_connection_request,dashboard_view, all_assistants , assistant_send_connection_request
urlpatterns = [
    # dashboard for agent and assistant
    path('agent-dashboard/', dashboard_view, name='dashboard'),
    # to see all homeowners
    path('all-homeowners/', all_homeowners, name='all_homeowners'),
    # to send invite to homeowners
    path('homeowner-send-connection-request/', homeowner_send_connection_request, name='homeowner_send_connection_request'),
    # to see all assistants
    path('all-assistants/', all_assistants, name='all_assistants'),
    # to send invite to assistants
    path('assistant-send-connection-request/', assistant_send_connection_request, name='assistant_send_connection_request'),
    # to see the status of request of homeowners
    path('homeowner-requests-status-by-agent/', homeowner_requests_status_by_agent, name='homeowner_requests_status_by_agent'),
    # to see the status of request of assistants
    path('assistant-requests-status-by-agent/', assistant_requests_status_by_agent, name='assistant_requests_status_by_agent'),
    # homeowner profile by agent pov
    path('homeowner/profile/', homeowner_profile, name='homeowner_profile'),
    # assistant profile by agent pov
    path('assistant/profile/', assistant_profile, name='assistant_profile'),
    # agent profile by agent pov
    path('profile/', agent_profile, name='agent_profile'),
    # agent profile view by agent
    path('profilebyID/<int:agent_id>/', agent_profile_by_ID, name='agent_profile_by_ID'),
    # all properties for agent dashbbaord
    path('all-agent-properties_dashboard',all_agent_properties_dashboard, name='all_agent_properties_dashboard'),
    # searched
    path('searched',searched, name='searched'),
    # send_connection_request_by_form
    path('send_connection_request_by_form/', send_connection_request_by_form, name='send_connection_request_by_form'),
    # register again
    path('signup-by-invite/<uuid:token>/', signup_by_invite, name='signup_by_invite'),

]
