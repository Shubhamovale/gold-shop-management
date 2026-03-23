from django.urls import path

from .views import register_view, verify_registration_otp_view

urlpatterns = [
    path('', register_view, name='register'),
    path('verify-otp/', verify_registration_otp_view, name='verify_registration_otp'),
]
