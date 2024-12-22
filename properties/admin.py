from django.contrib import admin
from .models import Property , ConnectionRequest,AgentInvitation

admin.site.register(Property)
admin.site.register(ConnectionRequest)
admin.site.register(AgentInvitation)