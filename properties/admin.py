from django.contrib import admin
from .models import Property , ConnectionRequest,AgentInvitation, Favorites

admin.site.register(Property)
admin.site.register(AgentInvitation)
admin.site.register(Favorites)