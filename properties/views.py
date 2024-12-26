from django.shortcuts import render , redirect, get_object_or_404
from users.models import Agent , Homeowner , Assistant
from .models import Property , ConnectionRequest
from django.contrib import messages
from .forms import PropertyForm
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
import stripe
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



# to create properties
def property_create(request):
    print("User authenticated:", request.user.is_authenticated)
    print("Session ID in redirected view:", request.session.session_key)
    try:
        homeowner = Homeowner.objects.get(user=request.user)
    except Homeowner.DoesNotExist:
        messages.error(request, "You must be a homeowner to create a property.")
        return redirect('home')

    property_count = Property.objects.filter(homeowner=homeowner).count()
    if property_count >= 10:
        messages.error(request, "You cannot upload more than 10 properties.")
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.homeowner = homeowner
            agent = Agent.objects.filter(homeowner=homeowner).first()
            property_obj.agent = agent
            property_obj.state = homeowner.user.state
            property_obj.assistant = agent.assistant if agent else None
            property_obj.approval_status = True if not agent else False
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
    active_subscription = None
    is_homeowner = False  # Default value
    
    if request.user.is_authenticated:
        active_subscription = request.user.subscription_set.filter(is_active=True, payment_successful=True).exists()
        is_homeowner = request.user.role == 'Homeowner'  # Check if the user is a homeowner
    
    return render(request, 'properties/listed_properties.html', {
        'properties': properties,
        'active_subscription': active_subscription,
        'is_homeowner': is_homeowner
    })

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
        if request.user.role == 'Agent':
            property_obj.assistant = agent.assistant
        else :
            property_obj.assistant = assistant
        property_obj.save()
        homeowner_email = property_obj.homeowner.user.email
        subject = 'Your Property has been Approved'
        message = f"Dear {property_obj.homeowner.user.name},\n\nYour property '{property_obj.address}' has been approved successfully!\n\nBest regards,\nThe Team"
        super_admin = User.objects.filter(role='SuperAdmin').first()
        if super_admin:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [super_admin.email])
        send_mail(subject, message, settings.EMAIL_HOST_USER, [homeowner_email])
        messages.success(request, "Property approved successfully.")
        return redirect('properties_tobe_approved')
    return render(request, 'properties/property_approve_confirm.html', {'property': property_obj})


# for properties_to_be_approved_by_assistant
def properties_to_be_approved_by_assistant(request):
    try:
        assistant_profile = Assistant.objects.get(user=request.user)
    except Assistant.DoesNotExist:
        messages.error(request, 'You need to be an assistant to view this page.')
        return redirect('home')

    agents = Agent.objects.filter(assistant=assistant_profile)

    if not agents:
        messages.error(request, 'You need to be assigned to at least one agent first.')
        return redirect('home')

    properties = Property.objects.filter(agent__in=agents, approval_status=False)

    if not properties:
        messages.info(request, "No properties available for approval.")

    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        property_to_approve = get_object_or_404(Property, id=property_id, agent__in=agents)
        property_to_approve.approval_status = True
        property_to_approve.save()
        messages.success(request, "Property has been approved successfully.")
        return redirect('properties_to_be_approved_by_assistant')

    return render(request, 'properties/properties_tobe_approved_by_assistant.html', {'properties': properties})

# property apporve by assistant
def property_approve_by_assistant(request, property_id):
    if request.user.role == 'Assistant':
        try:
            assistant_profile = Assistant.objects.get(user=request.user)
            property_obj = get_object_or_404(Property, id=property_id)
            agent_profile = property_obj.agent
            print(agent_profile)
            if agent_profile.assistant != assistant_profile:
                messages.error(request, 'You do not have permission to approve this property.')
                return redirect('home')
        except Assistant.DoesNotExist:
            messages.error(request, 'You need to be an assistant to approve properties.')
            return redirect('home')
    else:
        messages.error(request, "You do not have permission to approve this property.")
        return redirect('home')
    if request.method == 'POST':
        property_obj.approval_status = True
        property_obj.save()
        homeowner_email = property_obj.homeowner.user.email
        subject = 'Your Property has been Approved'
        message = f"Dear {property_obj.homeowner.user.name},\n\nYour property '{property_obj.address}' has been approved successfully!\n\nBest regards,\nThe Team"
        super_admin = User.objects.filter(role='SuperAdmin').first()
        if super_admin:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [super_admin.email])
        send_mail(subject, message, settings.EMAIL_HOST_USER, [homeowner_email])
        messages.success(request, "Property approved successfully on behalf of the agent.")
        return redirect('properties_to_be_approved_by_assistant')
    return render(request, 'properties/property_approve_confirm.html', {'property': property_obj})

# payment for property upload 
stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
def create_checkout_session(request):
    if request.method == 'GET':
        YOUR_DOMAIN = "http://127.0.0.1:8000" 
        print("Session before redirect:", request.session.session_key)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Property Upload Fee',
                    },
                    'unit_amount': 500,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=f'{YOUR_DOMAIN}/properties/create/',
            cancel_url=f'{YOUR_DOMAIN}',
        )
        return redirect(checkout_session.url, code=303)
    return JsonResponse({"error": "Invalid request"}, status=400)

# propery limit check
def check_property_limit(request):
    if request.user.is_authenticated:
        homeowner = Homeowner.objects.filter(user=request.user).first()
        if homeowner:
            property_count = Property.objects.filter(homeowner=homeowner).count()
            if property_count >= 10:
                messages.error(request, "You cannot upload more than 10 properties.")
                return redirect('home')
    return redirect('create_checkout_session')

# for property search
def property_search(request):
    query = request.GET.get('q')
    properties = Property.objects.all()
    
    if query:
        properties = properties.filter(state__icontains=query)

    return render(request, 'properties/property_search.html', {'properties': properties})

# Function that checks if a homeowner is assigned to an agent
def process_agent_homeowner(request):
    if not check_property_limit(request):
        return redirect('home')
    return create_checkout_session(request)
   

# property create by agent 
def agent_property_create(request):
    agent = Agent.objects.filter(user=request.user).first()
    if not agent:
        messages.error(request, "You must be logged in as an agent to create a property.")
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.homeowner = agent.homeowner if agent.homeowner else None
            property_obj.agent = agent
            property_obj.assistant = agent.assistant if agent.assistant else None
            # property_obj.state = agent.state if agent.homeowner else None
            property_obj.approval_status = True
            property_obj.save()
            messages.success(request, 'The property has been successfully created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form})

# Property create by assistant
def assistant_property_create(request):
    assistant = Assistant.objects.filter(user=request.user).first()
    if not assistant:
        messages.error(request, "You must be logged in as an assistant to create a property.")
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.homeowner = assistant.agents.first().homeowner if assistant.agents.exists() else None
            property_obj.assistant = assistant
            property_obj.agent = assistant.agents.first() if assistant.agents.exists() else None
            property_obj.approval_status = True
            property_obj.save()
            messages.success(request, 'The property has been successfully created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PropertyForm()

    return render(request, 'properties/property_form.html', {'form': form})
# alll fav
def favourites_list(request):
    properties = Property.objects.filter(favourites=True)
    return render(request, 'agent/fav.html', {'properties': properties})

# toggle fav
def toggle_favourite(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    property.favourites = not property.favourites
    property.save()
    return redirect('favourites_list')

# update
def update_property(request, pk):
    if not hasattr(request.user, 'agent_profile'):
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')

    property = get_object_or_404(Property, id=pk, agent=request.user.agent_profile)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('all_agent_properties_dashboard')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'agent/update_property.html', {'form': form})

# delete
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('all_agent_properties_dashboard')

# favv all
def favourite_properties(request):
    if not hasattr(request.user, 'agent_profile'):
        return render(request, 'error.html', {'message': 'You are not an agent.'})

    agent = request.user.agent_profile
    properties = Property.objects.filter(favourites=True, agent=agent)
    return render(request, 'agent/favprops.html', {'properties': properties})


# Update Property for Assistant
def assistant_update_property(request, pk):
    if not hasattr(request.user, 'assistant_profile'):
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')

    property = get_object_or_404(Property, id=pk, assistant=request.user.assistant_profile)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('all_assistant_properties_dashboard')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'agent/update_property.html', {'form': form})


# Delete Property for Assistant
def assistant_delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, assistant=request.user.assistant_profile)
    property.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('all_assistant_properties_dashboard')
