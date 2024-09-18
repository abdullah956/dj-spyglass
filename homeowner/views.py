from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest
from properties.forms import PropertyForm

def homeowner_invite_requests(request):
    homeowner = get_object_or_404(Homeowner, user=request.user)
    agents = Agent.objects.filter(user__state=homeowner.user.state)
    return render(request, 'homeowner/homeowner_invite_requests.html', {'agents': agents})

def homeownersend_connection_request(request):
    if request.user.role != 'Homeowner':
        messages.error(request, 'You must be a homeowner to send a connection request.')
        return redirect('homeowner_invite_requests')

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(Agent, id=agent_id)
        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=agent.user).exists()

        if existing_request:
            messages.error(request, 'You have already sent a connection request to this agent.')
        else:
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=agent.user
            )
            messages.success(request, 'Connection request sent to the agent.')

    return redirect('homeowner_invite_requests')
 
def property_create(request):
    try:
        homeowner = Homeowner.objects.get(user=request.user)
    except Homeowner.DoesNotExist:
        messages.error(request, "You must be a homeowner to create a property.")
        return redirect('home')

    connection = ConnectionRequest.objects.filter(sender=request.user, status='A').first()
    if not connection:
        messages.error(request, "You must make a connection with an agent before creating a property.")
        return redirect('home')

    try:
        agent = get_object_or_404(Agent, user=connection.receiver)
    except (ConnectionRequest.DoesNotExist, AttributeError):
        agent = None

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.homeowner = homeowner
            property_obj.agent = agent
            property_obj.state = homeowner.user.state
            property_obj.assistant = agent.assistant if agent else None
            property_obj.save()
            messages.success(request, f'{homeowner.user.username}, your property has been successfully created.')
            return redirect('homeowner_home')
        else:
            messages.error(request, f'{homeowner.user.username}, please correct the errors in the form.')
    else:
        form = PropertyForm()

    return render(request, 'homeowner/property_form.html', {'form': form})