from django.shortcuts import render ,redirect,get_object_or_404
from users.models import Agent
from properties.models import ConnectionRequest
from django.contrib import messages
from users.models import Assistant


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


def homeowner_connection_requests_all_agents(request):
    if request.user.role == 'Assistant':
        assistant = Assistant.objects.filter(user=request.user).first()
        print(assistant)
        if not assistant:
            messages.error(request, "No agent profile found for your account.")
            return redirect('dashboard')
        agents = Agent.objects.filter(assistant=assistant)
        print(agents)
        requests = ConnectionRequest.objects.filter(
            receiver__in=[agent.user for agent in agents],
            sender__role='Homeowner'
        )
        if not requests:
            messages.info(request, "No connection requests from homeowners are available for the agents you are connected to.")
    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('dashboard')

    return render(request, 'agent/homeowner_connection_requests.html', {'requests': requests})