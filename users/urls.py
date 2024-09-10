from django.urls import path
from .views import home_view , register_view , login_view , logout_view , verify_otp, password_reset_request, verify_otp_for_password_reset, password_change

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('verify-otp-for-password-reset/', verify_otp_for_password_reset, name='verify_otp_for_password_reset'),
    path('password-change/<int:user_id>/', password_change, name='password_change'),
]
