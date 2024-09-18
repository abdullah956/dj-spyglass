from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from users.models import User
from django.contrib.auth.forms import SetPasswordForm
from .models import Agent, Homeowner, Assistant, User
from .forms import CustomUserCreationForm

# for home 
def home_view(request):
    return render(request, 'home.html')

# to register
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user.role == 'Agent':
                Agent.objects.create(user=user)
            elif user.role == 'Homeowner':
                Homeowner.objects.create(user=user)
            elif user.role == 'Assistant':
                Assistant.objects.create(user=user)
            otp = pyotp.TOTP(settings.OTP_SECRET_KEY)
            otp_code = otp.now()
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            request.session['otp_email'] = user.email
            request.session['otp_code'] = otp_code
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# to login 
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('home')
            else:
                otp = pyotp.TOTP(settings.OTP_SECRET_KEY)
                otp_code = otp.now()
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_code}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                request.session['otp_email'] = user.email
                request.session['otp_code'] = otp_code
                return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'users/login.html')

# to logout
def logout_view(request):
    logout(request)
    return redirect('login')

# to verify login otp
def verify_otp(request):
    if request.method == 'POST':
        user_otp_code = request.POST.get('otp_code')
        session_otp_code = request.session.get('otp_code')
        email = request.session.get('otp_email')
        
        if user_otp_code == session_otp_code:
            try:
                user = User.objects.get(email=email)
                user.is_verified = True
                user.save()
                login(request, user)
                return redirect('home') 
            except User.DoesNotExist:
                return render(request, 'users/verify_otp.html', {'error': 'User not found'})
        else:
            return render(request, 'users/verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'users/verify_otp.html')

# to request password reset
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = pyotp.TOTP(settings.OTP_SECRET_KEY)
            otp_code = otp.now()
            send_mail(
                'Your OTP Code for Password Reset',
                f'Your OTP code is {otp_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            request.session['otp_email'] = user.email
            request.session['otp_code'] = otp_code

            return redirect('verify_otp_for_password_reset')
        except User.DoesNotExist:
            return render(request, 'users/password_reset_request.html', {'error': 'Email not found'})

    return render(request, 'users/password_reset_request.html')

# to verify password resert otp
def verify_otp_for_password_reset(request):
    if request.method == 'POST':
        user_otp_code = request.POST.get('otp_code')
        session_otp_code = request.session.get('otp_code')
        email = request.session.get('otp_email')

        if user_otp_code == session_otp_code:
            try:
                user = get_user_model().objects.get(email=email)
                return redirect('password_change', user_id=user.id)
            except get_user_model().DoesNotExist:
                return render(request, 'users/verify_otp_for_password_reset.html', {'error': 'User not found'})
        else:
            return render(request, 'users/verify_otp_for_password_reset.html', {'error': 'Invalid OTP'})
    return render(request, 'users/verify_otp_for_password_reset.html')

# to change password
def password_change(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=user.email, password=request.POST.get('new_password1'))
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try logging in again.')
    else:
        form = SetPasswordForm(user)
    return render(request, 'users/password_change.html', {'form': form})