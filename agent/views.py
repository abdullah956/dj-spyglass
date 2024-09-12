from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest
from django.shortcuts import render, get_object_or_404, redirect
from users.models import  Agent
from properties.models import Property
from properties.forms import PropertyForm


def agent_home_view(request):
    return render(request, 'agent/agent_home.html')

def connection_requests_view(request):
    requests = ConnectionRequest.objects.filter(
        receiver=request.user,
        sender__role='Homeowner'
    )
    return render(request, 'agent/connection_requests.html', {'requests': requests})


def update_request_status(request, request_id):
    if request.method == 'POST':
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest.STATUS_CHOICES):
            connection_request.status = new_status
            connection_request.save()
            return redirect('connection_requests')  
    return redirect('connection_requests')

def property_approval_list(request):
    agent = get_object_or_404(Agent, user=request.user)
    properties = Property.objects.filter(agent=agent, approval_status=False)
    return render(request, 'agent/property_approval_list.html', {'properties': properties})


def property_approve(request, property_id):
    agent = get_object_or_404(Agent, user=request.user)
    property_obj = get_object_or_404(Property, id=property_id, agent=agent)
    if request.method == 'POST':
        property_obj.approval_status = True
        property_obj.save()
        return redirect('property_approval_list') 
    return render(request, 'agent/property_approve_confirm.html', {'property': property_obj})

def assistant_connection_requests_view(request):
    requests = ConnectionRequest.objects.filter(
        receiver=request.user,
        sender__role='Assistant'
    )
    return render(request, 'agent/assistant_connection_requests.html', {'requests': requests})

def assistant_update_request_status(request, request_id):
    if request.method == 'POST':
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest.STATUS_CHOICES):
            connection_request.status = new_status
            connection_request.save()
            return redirect('assistant_connection_requests')  
    return redirect('assistant_connection_requests')