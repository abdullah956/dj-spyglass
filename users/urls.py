from django.urls import path
from .views import download_subscribers,subscribers_list,admin_dashboard,edit_profile, newsletter_view,contact_view,home_view , register_view , login_view , logout_view , verify_otp, password_reset_request, verify_otp_for_password_reset, password_change
urlpatterns = [
    # for home 
    path('', home_view, name='home'),
    # to register
    path('register/', register_view, name='register'),
    # to login
    path('login/', login_view, name='login'),
    # to logout
    path('logout/', logout_view, name='logout'),
    # to verify login otp
    path('verify-otp/', verify_otp, name='verify_otp'),
    # to request password reset
    path('password-reset/', password_reset_request, name='password_reset_request'),
    # to verfiy password otp
    path('verify-otp-for-password-reset/', verify_otp_for_password_reset, name='verify_otp_for_password_reset'),
    # to change password
    path('password-change/<int:user_id>/', password_change, name='password_change'),
    # for contact
    path('contact/', contact_view, name='contact'),
    # for newsletter
    path('newsletter/', newsletter_view, name='newsletter'),
    # edit profile
    path('edit-profile/', edit_profile, name='edit_profile'),
    # for admin
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    # for subscribers
    path('subscribers/', subscribers_list, name='subscribers_list'),
    # download subscribers
    path('subscribers/download/', download_subscribers, name='download_subscribers'),
]
