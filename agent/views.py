from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest
from django.shortcuts import render, get_object_or_404, redirect
from users.models import  Agent , Assistant
from properties.models import Property
from properties.forms import PropertyForm
from django.contrib import messages

def agent_home_view(request):
    return render(request, 'agent/agent_home.html')


def connection_requests_view(request):
    if request.user.role == 'Agent':
        requests = ConnectionRequest.objects.filter(
            receiver=request.user,
            sender__role='Homeowner'
        )
    else:
        accepted_request = ConnectionRequest.objects.filter(
            sender=request.user,
            status='A'
        ).first()
        if accepted_request:
            agent = Agent.objects.filter(user=accepted_request.receiver).first()
            print(agent)
            if agent:
                requests = ConnectionRequest.objects.filter(
                    receiver=agent.user,
                    sender__role='Homeowner'
                )
            else:
                requests = None
                messages.error(request, "No agent found related to the accepted request.")
        else:
            requests = None
            messages.error(request, "No accepted connection request found.")

    if not requests:
        messages.info(request, "No connection requests available.")

    return render(request, 'agent/connection_requests.html', {'requests': requests})



def update_request_status(request, request_id):
    if request.method == 'POST':
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest.STATUS_CHOICES):
            connection_request.status = new_status
            connection_request.save()
            messages.success(request, "Request status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")
    else:
        messages.warning(request, "Invalid request method.")
    
    return redirect('connection_requests')

def property_approval_list(request):
    if request.user.role == 'Agent':
        agent = get_object_or_404(Agent, user=request.user)
        properties = Property.objects.filter(agent=agent, approval_status=False)
    elif request.user.role == 'Assistant':
        assistant = get_object_or_404(Assistant, user=request.user)
        properties = Property.objects.filter(assistant=assistant, approval_status=False)
    else:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    if not properties:
        messages.info(request, "No properties available for approval.")

    return render(request, 'agent/property_approval_list.html', {'properties': properties})


def property_approve(request, property_id):
    if request.user.role == 'Agent':
        agent = get_object_or_404(Agent, user=request.user)
        property_obj = get_object_or_404(Property, id=property_id, agent=agent)
    elif request.user.role == 'Assistant':
        assistant = get_object_or_404(Assistant, user=request.user)
        property_obj = get_object_or_404(Property, id=property_id, assistant=assistant)
    else:
        messages.error(request, "You do not have permission to approve this property.")
        return redirect('home') 
    if request.method == 'POST':
        property_obj.approval_status = True
        property_obj.save()
        messages.success(request, "Property approved successfully.")
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
        print(connection_request.sender)
        print(new_status)
        if new_status in dict(ConnectionRequest.STATUS_CHOICES):
            if new_status == 'A':
                agent = get_object_or_404(Agent, user=request.user)
                assistant = get_object_or_404(Assistant, user=connection_request.sender)
                agent.assistant = assistant
                agent.save()
                messages.success(request, 'Connection request accepted and assistant added to the agent.')
            else:
                messages.info(request, 'Connection request status updated.')
            connection_request.status = new_status
            connection_request.save()
            return redirect('assistant_connection_requests')
    return redirect('assistant_connection_requests')


def dashboard_view(request):
    return render(request, 'agent/dashboard.html')