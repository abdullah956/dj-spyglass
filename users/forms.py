from django import forms
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm)

from .models import User


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': forms.CharField}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")
        field_classes = {'username': forms.CharField}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2', 'role', 'company', 'phone', 'state', 'business_address')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }