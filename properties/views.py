from django.shortcuts import render
from .models import Property

def approved_properties_view(request):
    properties = Property.objects.filter(approval_status=True)
    return render(request, 'listings.html', {'properties': properties})
