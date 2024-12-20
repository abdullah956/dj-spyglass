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
from django.core.mail import send_mail

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

    email_subject = 'Subscription Activated'
    email_body = (
        f'Hello {request.user.get_full_name()},\n\n'
        'We are thrilled to inform you that your subscription has been activated successfully!\n\n'
        f'**Subscription Details:**\n'
        f'- **Type:** {subscription.subscription_type.capitalize()}\n'
        f'- **Start Date:** {start_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
        f'- **End Date:** {end_date.strftime("%Y-%m-%d %H:%M:%S")}\n\n'
        'As a valued subscriber, you can enjoy the following benefits:\n'
        '- Access to premium content\n'
        '- Priority customer support\n'
        '- Regular updates and exclusive offers\n\n'
        'If you have any questions or need assistance, feel free to contact our support team at support@example.com.\n\n'
        'Thank you for choosing our service!\n\n'
        'Best Regards,\n'
        'The Team'
    )
    send_mail(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,  
        [request.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Subscription activated successfully!')
    return redirect('home')

# if subscription failed
def subscription_cancel(request):
    send_mail(
        'Subscription Canceled',
        'Your subscription has been canceled. If this was a mistake, please contact support.',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )
    messages.error(request, 'Subscription canceled. Please try again.')
    return redirect('home')

# for payment history
def payment_history(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/payment_history.html', {'subscriptions': subscriptions})

# subscription
def subscription_page(request):
    return render(request, 'subscriptions/subscription.html')