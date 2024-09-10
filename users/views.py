from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from users.models import User

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
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


def logout_view(request):
    logout(request)
    return redirect('login')


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