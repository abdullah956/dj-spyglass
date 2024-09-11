from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'price', 'state', 'bedrooms', 'bathrooms', 'process', 'compensation', 'square_feet', 'contract', 'property_images']