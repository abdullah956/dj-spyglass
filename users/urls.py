from django.urls import path
from .views import index_view , register_view

urlpatterns = [
    path('', index_view, name='index'),
    path('register/', register_view, name='register'),
]
