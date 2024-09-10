from django.shortcuts import render
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, 'base.html') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def index_view(request):
    return render(request, 'base.html')
