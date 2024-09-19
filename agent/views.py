from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest
from django.shortcuts import render, get_object_or_404, redirect
from users.models import  Agent , Assistant
from properties.models import Property
from django.contrib import messages
from users.models import User , Homeowner
from django.db.models import Count, Q


# for dashbaord
def dashboard_view(request):
    return render(request, 'agent/dashboard.html')


# to see all avaible homeowners
def all_homeowners(request):
    relevant_statuses = ['P', 'R']
    relevant_users = ConnectionRequest.objects.filter(
        status__in=relevant_statuses,
        receiver__in=Homeowner.objects.values_list('user', flat=True)
    ).values_list('receiver', flat=True)
    
    pending_rejected_homeowners = Homeowner.objects.filter(
        user__in=relevant_users
    )
    return render(request, 'agent/all_homeowners.html', {'homeowners': pending_rejected_homeowners})


# send connection to homeowner
def homeowner_send_connection_request(request):
    if request.method == 'POST':
        homeowner_id = request.POST.get('homeowner_id')
        homeowner = get_object_or_404(Homeowner, id=homeowner_id)
        agent_profile = Agent.objects.filter(user=request.user, assistant__isnull=False).exists()
        agent = get_object_or_404(Agent, user=request.user)
        if agent.homeowner:
            messages.error(request, 'You already have a connection with a homeowner.')
            return redirect('all_homeowners')
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


# to see all available assistants
def all_assistants(request):
    relevant_statuses = ['P', 'R']
    assistants_with_relevant_requests = Assistant.objects.filter(
        user__in=ConnectionRequest.objects.filter(
            status__in=relevant_statuses
        ).values_list('receiver', flat=True)
    ).distinct()
    assistant_ids_with_one_accepted_request = ConnectionRequest.objects.filter(
        status='A'
    ).values('receiver').annotate(
        num_accepted_requests=Count('id')
    ).filter(
        num_accepted_requests=1
    ).values_list('receiver', flat=True)
    assistants_with_one_accepted_request = Assistant.objects.filter(
        user__in=assistant_ids_with_one_accepted_request
    ).distinct()
    assistants_to_display = assistants_with_relevant_requests | assistants_with_one_accepted_request
    return render(request, 'agent/all_assistants.html', {'assistants': assistants_to_display})

# send connection to assistant
def assistant_send_connection_request(request):
    if request.method == 'POST':
        assistant_id = request.POST.get('assistant_id')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=assistant.user).exists()
        agent = get_object_or_404(Agent, user=request.user)
        if agent.homeowner:
            messages.error(request, 'You already have a connection with a assistant.')
            return redirect('all_assistants')
        if existing_request:
            messages.error(request, 'You have already sent a connection request to this assistant.')
        else:
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=assistant.user
            )
            messages.success(request, 'Connection request sent to the assistant.')
    return redirect('all_assistants')


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

# homeowner profile
def homeowner_profile(request):
    user = request.user
    try:
        agent = Agent.objects.get(user=user)
        if agent.homeowner is None:
            messages.error(request, "Homeowner profile not found.")
            return redirect('dashboard')
        homeowner = agent.homeowner
    except Agent.DoesNotExist:
        messages.error(request, "Agent profile not found.")
        return redirect('dashboard')
    except Homeowner.DoesNotExist:
        messages.error(request, "Homeowner profile not found.")
        return redirect('dashboard')
    return render(request, 'agent/homeowner_profile.html', {'homeowner': homeowner})

# assistant profile
def assistant_profile(request):
    user = request.user
    try:
        agent = Agent.objects.get(user=user)
        if agent.assistant is None:
            messages.error(request, "Assistant profile not found.")
            return redirect('dashboard')
        assistant = agent.assistant
    except Agent.DoesNotExist:
        messages.error(request, "Agent profile not found.")
        return redirect('dashboard') 
    except Assistant.DoesNotExist:
        messages.error(request, "Assistant profile not found.")
        return redirect('dashboard') 
    return render(request, 'agent/assistant_profile.html', {'assistant': assistant})

# agent profile
def agent_profile(request):
    user = request.user
    agent = Agent.objects.get(user=user)
    return render(request, 'agent/agent_profile.html', {'agent': agent})