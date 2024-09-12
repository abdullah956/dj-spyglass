from django.urls import path
from .views import approved_properties_view

urlpatterns = [
    path('approved-properties/', approved_properties_view, name='approved_properties'),
]
