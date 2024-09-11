from django.shortcuts import render,redirect, get_object_or_404, redirect, get_object_or_404
from properties.models import ConnectionRequest


def agent_home_view(request):
    return render(request, 'agent/agent_home.html')

def connection_requests_view(request):
    requests = ConnectionRequest.objects.filter(receiver=request.user)
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