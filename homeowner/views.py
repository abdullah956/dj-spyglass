from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest
from properties.forms import PropertyForm


# to show all agent invites to homeowner
def agents_invites(request):
    current_user = request.user
    requests = ConnectionRequest.objects.filter(receiver=current_user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        connection_request = ConnectionRequest.objects.get(id=request_id)
        connection_request.status = new_status
        connection_request.save()
        return redirect('agent_invites')
    return render(request, 'homeowner/agent_invites.html', {'requests': requests})