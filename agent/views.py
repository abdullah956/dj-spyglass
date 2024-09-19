from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest
from django.shortcuts import render, get_object_or_404, redirect
from users.models import  Agent , Assistant
from properties.models import Property
from django.contrib import messages
from users.models import User , Homeowner

# for dashbaord
def dashboard_view(request):
    return render(request, 'agent/dashboard.html')

# to see all homeowners
def all_homeowners(request):
    Homeowners = Homeowner.objects.filter()
    return render(request, 'agent/all_homeowners.html', {'homeowners': Homeowners})

# send connection to homeowner
def homeowner_send_connection_request(request):
    if request.method == 'POST':
        homeowner_id = request.POST.get('homeowner_id')
        homeowner = get_object_or_404(Homeowner, id=homeowner_id)
        agent_profile = Agent.objects.filter(user=request.user, assistant__isnull=False).exists()
        if not agent_profile:
            messages.error(request, 'You must have an assigned assistant before sending a connection request to a homeowner.')
            return redirect('all_homeowners')
        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=homeowner.user).exists()
        if existing_request:
            messages.error(request, 'You have already sent a connection request to this homeowner.')
        else:
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=homeowner.user
            )
            messages.success(request, 'Connection request sent to the homeowner.')
    return redirect('all_homeowners')


# to see all assistants
def all_assistants(request):
    Assistants = Assistant.objects.filter()
    return render(request, 'agent/all_assistants.html', {'assistants': Assistants})


# send connection to assistant
def assistant_send_connection_request(request):
    if request.method == 'POST':
        assistant_id = request.POST.get('assistant_id')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=assistant.user).exists()

        if existing_request:
            messages.error(request, 'You have already sent a connection request to this assistant.')
        else:
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=assistant.user
            )
            messages.success(request, 'Connection request sent to the assistant.')
    return redirect('all_homeowners')

# homeowner_requests_status_by_agent 
def homeowner_requests_status_by_agent(request):
    if request.user.role == 'Agent':
        connection_requests = ConnectionRequest.objects.filter(
            sender=request.user,
            receiver__in=Homeowner.objects.values_list('user', flat=True)
        )
    else:
        connection_requests = []
    homeowner_statuses = []
    for req in connection_requests:
        try:
            homeowner = get_object_or_404(Homeowner, user=req.receiver)
            status_display = req.get_status_display()
            homeowner_statuses.append({
                'homeowner': homeowner,
                'status': status_display
            })
        except Homeowner.DoesNotExist:
            continue
    return render(request, 'agent/homeowner_requests_status_by_agent.html', {'homeowner_statuses': homeowner_statuses})



# assistant_requests_status_by_agent 
def assistant_requests_status_by_agent(request):
    if request.user.role == 'Agent':
        connection_requests = ConnectionRequest.objects.filter(
            sender=request.user,
            receiver__in=Assistant.objects.values_list('user', flat=True)
        )
    else:
        connection_requests = []
    assistant_statuses = []
    for req in connection_requests:
        try:
            assistant = get_object_or_404(Assistant, user=req.receiver)
            status_display = req.get_status_display()
            assistant_statuses.append({
                'assistant': assistant,
                'status': status_display
            })
        except Homeowner.DoesNotExist:
            continue
    return render(request, 'agent/assistant_requests_status_by_agent.html', {'assistant_statuses': assistant_statuses})