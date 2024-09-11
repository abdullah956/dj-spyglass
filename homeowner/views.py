from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Agent 

def homeowner_home_view(request):
    return render(request, 'homeowner/homeowner_home.html')

def list_agents(request):
    agents = Agent.objects.all()
    return render(request, 'homeowner/list_agents.html', {'agents': agents})

