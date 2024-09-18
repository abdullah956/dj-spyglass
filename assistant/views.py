from django.shortcuts import render ,redirect,get_object_or_404
from users.models import Agent
from properties.models import ConnectionRequest
from django.contrib import messages
from users.models import Assistant
def assistant_home_view(request):
    return render(request, 'assistant/assistant_home.html')


def asssistant_invite_requests(request):
    assistant = get_object_or_404(Assistant, user=request.user)
    agents = Agent.objects.filter(user__state=assistant.user.state)
    return render(request, 'assistant/asssistant_invite_requests.html', {'agents': agents})


def send_connection_request(request):
    if request.user.role != 'Assistant':
        messages.error(request, 'You must be an assistant to send a connection request.')
        return redirect('asssistant_invite_requests')

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(Agent, id=agent_id)

        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=agent.user).exists()

        if existing_request:
            messages.error(request, 'You have already sent a connection request to this agent.')
        else:
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=agent.user
            )
            messages.success(request, 'Connection request sent to the agent.')

    return redirect('asssistant_invite_requests')

