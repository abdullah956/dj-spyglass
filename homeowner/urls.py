from django.urls import path
from .views import homeowner_home_view

urlpatterns = [
    path('', homeowner_home_view, name='homeowner_home'),

]
