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