from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import stripe
from datetime import timedelta
from .models import Subscription
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone

stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

# for subscription page
def subscription_view(request):
    return render(request, 'subscriptions/subscribe.html')

# for subscription of assistant
def subscribe_assistant(request, subscription_type):
    if subscription_type == 'monthly':
        amount = 200
        duration = timedelta(days=30)
    elif subscription_type == 'yearly':
        amount = 2000
        duration = timedelta(days=365)
    else:
        messages.error(request, 'Invalid subscription type.')
        return redirect('home')
    start_date = timezone.now()
    end_date = start_date + duration
    subscription = Subscription.objects.create(
        user=request.user,
        subscription_type=subscription_type,
        is_active=False,
        amount=amount / 100,
        start_date=start_date,  
        end_date=end_date, 
        payment_successful=False
    )
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'{subscription_type.capitalize()} Subscription',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('subscription_success', args=[subscription.id])
        ),
        cancel_url=request.build_absolute_uri(reverse('subscription_cancel')),
    )
    return redirect(checkout_session.url, code=303)

# for subscription of agent
def subscribe_agent(request, subscription_type):
    if subscription_type == 'monthly':
        amount = 1000
        duration = timedelta(days=30)
    elif subscription_type == 'yearly':
        amount = 10000
        duration = timedelta(days=365)
    else:
        messages.error(request, 'Invalid subscription type.')
        return redirect('home')
    start_date = timezone.now()
    end_date = start_date + duration
    subscription = Subscription.objects.create(
        user=request.user,
        subscription_type=subscription_type,
        is_active=False,
        amount=amount / 100,
        start_date=start_date,  
        end_date=end_date, 
        payment_successful=False
    )
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'{subscription_type.capitalize()} Subscription',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('subscription_success', args=[subscription.id])
        ),
        cancel_url=request.build_absolute_uri(reverse('subscription_cancel')),
    )
    return redirect(checkout_session.url, code=303)


# if subscription successfull
def subscription_success(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    if subscription.payment_successful and subscription.is_active:
        messages.error(request, 'Subscription already active.')
        return redirect('home')
    start_date = timezone.now()
    if subscription.subscription_type == 'monthly':
        end_date = start_date + timedelta(days=30)
    else:
        end_date = start_date + timedelta(days=365)
    subscription.start_date = start_date
    subscription.end_date = end_date
    subscription.payment_successful = True
    subscription.is_active = True
    subscription.save()
    messages.success(request, 'Subscription activated successfully!')
    return redirect('home')

# if subscription failed
def subscription_cancel(request):
    messages.error(request, 'Subscription canceled. Please try again.')
    return redirect('home')
