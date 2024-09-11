from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest


def homeowner_home_view(request):
    return render(request, 'homeowner/homeowner_home.html')

def list_agents(request):
    agents = Agent.objects.all()
    return render(request, 'homeowner/list_agents.html', {'agents': agents})


def send_connection_request(request):
    if not request.user.role == 'Homeowner':
        messages.error(request, 'You must be a homeowner to send a connection request.')
        return redirect('list_agents')

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(Agent, id=agent_id)

        ConnectionRequest.objects.create(
            sender=request.user,
            receiver=agent.user
        )

        messages.success(request, 'Connection request sent to the agent.')
    
    return redirect('list_agents')