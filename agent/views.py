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
    agent = get_object_or_404(Agent, user=request.user)
    Homeowners = Homeowner.objects.filter(user__state=agent.user.state)
    return render(request, 'agent/all_homeowners.html', {'homeowners': Homeowners})


# send connection to homeowner
def homeowner_send_connection_request(request):
    if request.method == 'POST':
        homeowner_id = request.POST.get('homeowner_id')
        homeowner = get_object_or_404(Homeowner, id=homeowner_id)
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
