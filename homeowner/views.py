from django.shortcuts import render

def homeowner_home_view(request):
    return render(request, 'homeowner/homeowner_home.html')