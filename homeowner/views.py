from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Agent, Homeowner
from properties.models import ConnectionRequest
from properties.forms import PropertyForm


# to see all invites form the agents and update process
def agent_invites_for_homeowner(request):
    current_user = request.user
    requests = ConnectionRequest.objects.filter(receiver=current_user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        try:
            connection_request = ConnectionRequest.objects.get(id=request_id, receiver=current_user)
            agent = Agent.objects.get(user=connection_request.sender)
            homeowner = Homeowner.objects.get(user=current_user)
            if agent.homeowner and agent.homeowner != homeowner:
                messages.error(request, 'The agent already has a homeowner assigned and cannot entertain more requests.')
                return redirect('agent_invites_for_homeowner')
            connection_request.status = new_status
            connection_request.save()
            if new_status == 'A':
                if agent.homeowner and agent.homeowner != homeowner:
                    messages.error(request, 'The agent is already connected to another homeowner. Cannot update.')
                else:
                    agent.homeowner = homeowner
                    agent.save()
                    messages.success(request, 'Connection request approved and homeowner assigned to the agent.')
            elif new_status in ['P', 'R']:
                if agent.homeowner == homeowner:
                    agent.homeowner = None
                    agent.save()
                    messages.info(request, 'Connection request updated, homeowner removed from agent.')
        except ConnectionRequest.DoesNotExist:
            messages.error(request, 'Connection request not found.')
        except Homeowner.DoesNotExist:
            messages.error(request, 'Homeowner profile not found.')
        return redirect('agent_invites_for_homeowner')
    return render(request, 'homeowner/agent_invites_for_homeowner.html', {'requests': requests})

# email acceptance
def email_accept_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id)
    agent = get_object_or_404(Agent, user=connection_request.sender)

    homeowner = connection_request.receiver.homeowner_profile 
    if agent.homeowner:
        messages.error(request, 'This agent is already connected to a homeowner.')
    elif not homeowner:
        messages.error(request, 'Homeowner profile not found for the receiver.')
    else:
        agent.homeowner = homeowner  
        agent.save()
        connection_request.status = 'A'  
        connection_request.save()
        messages.success(request, 'You have successfully accepted the connection request.')
    
    return redirect('home')