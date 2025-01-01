from django.urls import path
from .views import property_detail, assistant_delete_property,assistant_update_property,assistant_property_create,favourite_properties,delete_property,update_property,toggle_favourite,favourites_list,process_agent_homeowner,agent_property_create,property_search,check_property_limit,create_checkout_session,listed_properties , properties_tobe_approved , property_approve , property_create,properties_to_be_approved_by_assistant,property_approve_by_assistant

urlpatterns = [
    # to create properties
    path('create/', property_create, name='property_create'),
    # listed properties
    path('listed-properties/', listed_properties , name='listed_properties'),
    # to see all property
    path('properties-tobe-approved', properties_tobe_approved, name='properties_tobe_approved'),
    # to approve property
    path('approve/<int:property_id>/', property_approve, name='property_approve'),
    # to see all property for assistant
    path('properties-tobe-approved-by-assistant', properties_to_be_approved_by_assistant, name='properties_to_be_approved_by_assistant'),
    # to approve property by assistant
    path('property-approve-by-assistant/<int:property_id>/', property_approve_by_assistant, name='property_approve_by_assistant'),
    # stripe fee upload 
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('check-limit/', check_property_limit, name='check_property_limit'),
    # for search
    path('search/', property_search, name='property_search'),
    # process agent
    path('process-agent/', process_agent_homeowner, name='process_agent_homeowner'),
    # property create by agent 
    path('property-create-by-agent/',agent_property_create , name='agent_property_create'),
    # property create by assistant
    path('assistant/property/create/', assistant_property_create, name='assistant_property_create'),
    # fav 
    path('favourites/', favourites_list, name='favourites_list'),
    # toggle fav
    path('toggle-favourite/<int:property_id>/', toggle_favourite, name='toggle_favourite'),
    # update
    path('properties/<int:pk>/update/', update_property, name='update_property'),
    # delete
    path('properties/<int:pk>/delete/', delete_property, name='delete_property'),
    # fav only
    path('favourite/', favourite_properties, name='favourite_properties'),
    # update ass
    path('assistant/update-property/<int:pk>/', assistant_update_property, name='assistant_update_property'),
    # delete ass
    path('assistant/delete-property/<int:pk>/', assistant_delete_property, name='assistant_delete_property'),
    path('<int:id>/', property_detail, name='property_detail'),
    ]