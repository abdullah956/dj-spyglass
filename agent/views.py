from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest
from django.shortcuts import render, get_object_or_404, redirect
from users.models import  Agent , Assistant
from properties.models import Property
from django.contrib import messages
from users.models import User , Homeowner
from django.db.models import Count, Q
from subscriptions.models import Subscription

# for dashbaord
def dashboard_view(request):
    subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
    if subscription:
        context = {}
        if request.user.role == 'Agent':
            agent = Agent.objects.filter(user=request.user).first()
            if agent:
                homeowner = agent.homeowner
                assistant = agent.assistant
                properties = Property.objects.filter(agent=agent)
                context = {
                    'user_role': 'Agent',
                    'homeowner': homeowner,
                    'assistant' : assistant,
                    'properties_count': properties.count(),
                }
        
        elif request.user.role == 'Assistant':
            assistant = Assistant.objects.filter(user=request.user).first()
            if assistant:
                connected_agents = Agent.objects.filter(assistant=assistant)
                properties_count = sum(Property.objects.filter(agent=agent).count() for agent in connected_agents)
                context = {
                    'user_role': 'Assistant',
                    'connected_agents': connected_agents,
                    'properties_count': properties_count,
                }
        return render(request, 'agent/dashboard_landing_agent_assistant.html', context)
    else:
        messages.error(request, "Please buy a subscription to access the dashboard.")
        return redirect('home')
    
# to see all avaible homeowners
def all_homeowners(request):
    relevant_statuses = ['P', 'R']
    excluded_users = ConnectionRequest.objects.filter(
        status__in=relevant_statuses,
        receiver__in=Homeowner.objects.values_list('user', flat=True)
    ).values_list('receiver', flat=True)
    
    homeowners = Homeowner.objects.exclude(user__in=excluded_users)
    
    return render(request, 'agent/all_homeowners.html', {'homeowners': homeowners})


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
    excluded_assistants = ConnectionRequest.objects.filter(
        status__in=relevant_statuses
    ).values_list('receiver', flat=True)

    assistants_with_more_than_one_accepted = ConnectionRequest.objects.filter(
        status='A'
    ).values('receiver').annotate(
        num_accepted_requests=Count('id')
    ).filter(
        num_accepted_requests__gt=1
    ).values_list('receiver', flat=True)

    assistants_to_display = Assistant.objects.exclude(
        user__in=excluded_assistants
    ).exclude(
        user__in=assistants_with_more_than_one_accepted
    )

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

# agent profile by id\
def agent_profile_by_ID(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    return render(request, 'agent/agent_profile_by_ID.html', {'agent': agent})