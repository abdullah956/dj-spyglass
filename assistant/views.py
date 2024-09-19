from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner , Assistant
from properties.models import ConnectionRequest
from properties.forms import PropertyForm

# to see all invites form the agents and update process
def agent_invites_for_assistant(request):
    current_user = request.user
    requests = ConnectionRequest.objects.filter(receiver=current_user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        try:
            connection_request = ConnectionRequest.objects.get(id=request_id, receiver=current_user)
            connection_request.status = new_status
            connection_request.save()
            assistant = Assistant.objects.get(user=current_user)
            if new_status == 'A':
                Agent.objects.update_or_create(
                    user=connection_request.sender,
                    defaults={'assistant': assistant}
                )
            elif new_status in ['P', 'R']:
                agent = Agent.objects.filter(user=connection_request.sender).first()
                if agent and agent.assistant == assistant:
                    agent.assistant = None
                    agent.save()
        except (ConnectionRequest.DoesNotExist, Assistant.DoesNotExist):
            pass
        return redirect('agent_invites_for_assistant')
    return render(request, 'assistant/agent_invites_for_assistant.html', {'requests': requests})

# to see all homeowners for the agent
def all_homeowners_for_assistant(request):
    try:
        assistant_profile = Assistant.objects.get(user=request.user)
        agent_profile = Agent.objects.get(assistant=assistant_profile)
    except Assistant.DoesNotExist:
        messages.error(request, 'You need to be an assistant to view this page.')
        return redirect('home')
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be assigned to an agent first.')
        return redirect('home')
    homeowners = Homeowner.objects.all()
    context = {
        'homeowners': homeowners,
    }
    return render(request, 'assistant/all_homeowners_for_assistant.html', context)

# send connection requests to homeowenrs by the assistant
def assistant_send_connection_request_homeowner(request):
    try:
        assistant_profile = Assistant.objects.get(user=request.user)
        agent_profile = Agent.objects.get(assistant=assistant_profile)
    except Assistant.DoesNotExist:
        messages.error(request, 'You need to be an assistant to view this page.')
        return redirect('home')
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be assigned to an agent first.')
        return redirect('home')
    if request.method == 'POST':
        homeowner_id = request.POST.get('homeowner_id')
        homeowner = get_object_or_404(Homeowner, id=homeowner_id)
        existing_request = ConnectionRequest.objects.filter(sender=agent_profile.user, receiver=homeowner.user).exists()
        if existing_request:
            messages.error(request, 'A connection request has already been sent to this homeowner.')
        else:
            ConnectionRequest.objects.create(
                sender=agent_profile.user,
                receiver=homeowner.user
            )
            messages.success(request, 'Connection request sent on behalf of the agent.')
    homeowners = Homeowner.objects.all()
    context = {
        'homeowners': homeowners,
    }
    return render(request, 'assistant/all_homeowners_for_assistant.html', context)