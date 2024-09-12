from django.contrib import admin
from django.urls import path , include
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('homeowner/',include('homeowner.urls')),
    path('agent/',include('agent.urls')),
    path('assistant/',include('assistant.urls')),
    path('properties/',include('properties.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
