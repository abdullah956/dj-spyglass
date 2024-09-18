from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest
from properties.forms import PropertyForm
 
# to create properties
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

# to update the requests of agent
def agent_update_request_status(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        
        connection_request = get_object_or_404(ConnectionRequest, id=request_id)
        connection_request.status = new_status
        connection_request.save()
        
        return redirect('agent_invites')

    return redirect('agent_invites')