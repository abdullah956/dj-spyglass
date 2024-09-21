from django.shortcuts import render

def subscription_view(request):
    return render(request, 'subscriptions/subscribe.html')