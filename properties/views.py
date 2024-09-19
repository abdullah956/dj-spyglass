from django.shortcuts import render , redirect, get_object_or_404
from users.models import Agent , Homeowner , Assistant
from .models import Property , ConnectionRequest
from django.contrib import messages
from .forms import PropertyForm

# to create properties
def property_create(request):
    try:
        homeowner = Homeowner.objects.get(user=request.user)
    except Homeowner.DoesNotExist:
        messages.error(request, "You must be a homeowner to create a property.")
        return redirect('home')
    agent = Agent.objects.filter(homeowner=homeowner).first()
    
    if not agent:
        messages.error(request, "You must be connected with an agent before creating a property.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.homeowner = homeowner
            property_obj.agent = agent
            property_obj.state = homeowner.user.state
            property_obj.assistant = agent.assistant
            property_obj.save()
            messages.success(request, 'Your property has been successfully created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {'form': form})

# listed properties
def listed_properties(request):
    properties = Property.objects.filter(approval_status=True)
    return render(request, 'properties/listed_properties.html', {'properties': properties})


# property lists of agents
def properties_tobe_approved(request):
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

    return render(request, 'properties/properties_tobe_approved.html', {'properties': properties})

# approve property
def property_approve(request, property_id):
    if request.user.role == 'Agent':
        agent = get_object_or_404(Agent, user=request.user)
        if agent.assistant is None:
            messages.error(request, "You must have an assigned assistant to approve properties.")
            return redirect('properties_tobe_approved')
        property_obj = get_object_or_404(Property, id=property_id, agent=agent)
    elif request.user.role == 'Assistant':
        assistant = get_object_or_404(Assistant, user=request.user)
        property_obj = get_object_or_404(Property, id=property_id, assistant=assistant)
    else:
        messages.error(request, "You do not have permission to approve this property.")
        return redirect('home')
    
    if request.method == 'POST':
        property_obj.approval_status = True
        property_obj.assistant = agent.assistant
        property_obj.save()
        messages.success(request, "Property approved successfully.")
        return redirect('properties_tobe_approved')
    return render(request, 'properties/property_approve_confirm.html', {'property': property_obj})

