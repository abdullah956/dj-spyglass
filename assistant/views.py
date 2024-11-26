from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner , Assistant
from properties.models import ConnectionRequest
from properties.forms import PropertyForm
from properties.models import Property

# to see all invites form the agents and update process
def agent_invites_for_assistant(request):
    current_user = request.user
    requests = ConnectionRequest.objects.filter(receiver=current_user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        try:
            connection_request = ConnectionRequest.objects.get(id=request_id, receiver=current_user)
            agent = Agent.objects.get(user=connection_request.sender)
            assistant = Assistant.objects.get(user=current_user)
            assigned_agents_count = Agent.objects.filter(assistant=assistant).count()
            if new_status == 'A' and assigned_agents_count >= 2:
                messages.error(request, 'You cannot accept more than 2 connection requests as an assistant.')
                return redirect('agent_invites_for_assistant')
            if agent.assistant and agent.assistant != assistant:
                messages.error(request, 'The agent is already connected to another assistant and cannot entertain this request.')
                return redirect('agent_invites_for_assistant')
            connection_request.status = new_status
            connection_request.save()
            if new_status == 'A':
                agent.assistant = assistant
                agent.save()
                messages.success(request, 'Connection request approved and assistant assigned to the agent.')
            elif new_status in ['P', 'R']:
                if agent.assistant == assistant:
                    agent.assistant = None
                    agent.save()
                    messages.info(request, 'Connection request updated, assistant removed from agent.')
        except ConnectionRequest.DoesNotExist:
            messages.error(request, 'Connection request not found.')
        except Assistant.DoesNotExist:
            messages.error(request, 'Assistant profile not found.')
        return redirect('agent_invites_for_assistant')
    return render(request, 'assistant/agent_invites_for_assistant.html', {'requests': requests})

# to see all availablen homeowners for the assistant
# def all_homeowners_for_assistant(request):
#     try:
#         assistant_profile = get_object_or_404(Assistant, user=request.user)
#         agent_profile = get_object_or_404(Agent, assistant=assistant_profile)
#     except Assistant.DoesNotExist:
#         messages.error(request, 'You need to be an assistant to view this page.')
#         return redirect('home')
#     except Agent.DoesNotExist:
#         messages.error(request, 'You need to be assigned to an agent first.')
#         return redirect('home')
#     homeowners_with_requests = Homeowner.objects.filter(
#         user__in=ConnectionRequest.objects.filter(
#             status__in=['P', 'R'],
#             sender=agent_profile.user
#         ).values_list('receiver', flat=True)
#     )
#     context = {
#         'homeowners': homeowners_with_requests,
#     }
#     return render(request, 'assistant/all_homeowners_for_assistant.html', context)

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
    if agent_profile.homeowner:
            messages.error(request, 'You already have a connection with a homeowner.')
            return redirect('all_homeowners_for_assistant')
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


# homeowner request status assistant pov
def homeowner_requests_status_by_assistant(request):
    assistant_profile = get_object_or_404(Assistant, user=request.user)
    agents = Agent.objects.filter(assistant=assistant_profile)
    connection_requests = ConnectionRequest.objects.filter(
        sender__in=agents.values_list('user', flat=True),
        receiver__in=Homeowner.objects.values_list('user', flat=True)
    )
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
    return render(request, 'assistant/homeowner_requests_status_by_assistant.html', {'homeowner_statuses': homeowner_statuses})

# all properties for assistant
def all_assistant_properties_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view properties.")
        return redirect('login')

    properties = Property.objects.filter(assistant__user=request.user)
    return render(request, 'assistant/all_properties_of_assistant.html', {'properties': properties})