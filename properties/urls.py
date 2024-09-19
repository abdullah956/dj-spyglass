from django.urls import path
from .views import listed_properties , properties_tobe_approved , property_approve , property_create,properties_to_be_approved_by_assistant,property_approve_by_assistant

urlpatterns = [
    # to create properties
    path('create/', property_create, name='property_create'),
    # listed properties
    path('listed_properties/', listed_properties , name='listed_properties'),
    # to see all property
    path('properties-tobe-approved', properties_tobe_approved, name='properties_tobe_approved'),
    # to approve property
    path('approve/<int:property_id>/', property_approve, name='property_approve'),
    # to see all property for assistant
    path('properties-tobe-approved-by-assistant', properties_to_be_approved_by_assistant, name='properties_to_be_approved_by_assistant'),
    # to approve property by assistant
    path('property_approve_by_assistant/<int:property_id>/', property_approve_by_assistant, name='property_approve_by_assistant'),
]
