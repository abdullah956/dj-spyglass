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
    agent = Agent.objects.filter(homeowner=homeowner).first()
    if not agent:
        messages.error(request, "You must be connected with an agent before creating a property.")
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