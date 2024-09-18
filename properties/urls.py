from django.urls import path
from .views import listed_properties , properties_tobe_approved , property_approve , property_create

urlpatterns = [
    # to create properties
    path('create/', property_create, name='property_create'),
    # listed properties
    path('listed_properties/', listed_properties , name='listed_properties'),
    # to see all property
    path('properties-tobe-approved', properties_tobe_approved, name='properties_tobe_approved'),
    # to approve property
    path('approve/<int:property_id>/', property_approve, name='property_approve'),
]
