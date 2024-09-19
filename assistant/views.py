from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest
from properties.forms import PropertyForm

# to show all agent invites to assistant
def agent_invites_for_assistant(request):
    current_user = request.user
    requests = ConnectionRequest.objects.filter(receiver=current_user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        connection_request = ConnectionRequest.objects.get(id=request_id)
        connection_request.status = new_status
        connection_request.save()
        return redirect('agent_invites_for_assistant')
    return render(request, 'assistant/agent_invites_for_assistant.html', {'requests': requests})