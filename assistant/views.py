from django.shortcuts import render ,redirect,get_object_or_404
from users.models import Agent
from properties.models import ConnectionRequest
from django.contrib import messages

def assistant_home_view(request):
    return render(request, 'assistant/assistant_home.html')

def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'assistant/agents_list.html', {'agents': agents})


def send_connection_request(request):
    if not request.user.role == 'Assistant':
        messages.error(request, 'You must be a assistant to send a connection request.')
        return redirect('agents_list')

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(Agent, id=agent_id)

        ConnectionRequest.objects.create(
            sender=request.user,
            receiver=agent.user
        )

        messages.success(request, 'Connection request sent to the agent.')
    
    return redirect('agents_list')