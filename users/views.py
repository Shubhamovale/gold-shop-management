from datetime import datetime, timedelta
import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import OTPVerificationForm, RegisterForm

OTP_SESSION_KEY = 'pending_registration'
OTP_EXPIRY_MINUTES = 10


def _generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


def _store_pending_registration(request, cleaned_data, otp_code):
    request.session[OTP_SESSION_KEY] = {
        'form_data': {
            'username': cleaned_data['username'],
            'email': cleaned_data['email'],
            'password1': cleaned_data['password1'],
            'password2': cleaned_data['password2'],
        },
        'otp_hash': make_password(otp_code),
        'otp_expires_at': (timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat(),
    }
    request.session.modified = True


def _send_registration_otp(email, otp_code):
    send_mail(
        subject='Gold Shop verification code',
        message=(
            f'Your Gold Shop OTP is {otp_code}. '
            f'It will expire in {OTP_EXPIRY_MINUTES} minutes.'
        ),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        recipient_list=[email],
        fail_silently=False,
    )


def _get_pending_registration(request):
    return request.session.get(OTP_SESSION_KEY)


def _clear_pending_registration(request):
    if OTP_SESSION_KEY in request.session:
        del request.session[OTP_SESSION_KEY]
        request.session.modified = True

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            otp_code = _generate_otp()
            _store_pending_registration(request, form.cleaned_data, otp_code)

            try:
                _send_registration_otp(form.cleaned_data['email'], otp_code)
            except Exception:
                _clear_pending_registration(request)
                form.add_error('email', 'We could not send the OTP email right now. Please try again later.')
            else:
                messages.success(request, 'We sent a 6-digit OTP to your email. Enter it below to finish registration.')
                return redirect('verify_registration_otp')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def verify_registration_otp_view(request):
    pending = _get_pending_registration(request)

    if not pending:
        messages.info(request, 'Start registration first, then verify the OTP from your email.')
        return redirect('register')

    if request.method == 'POST' and request.POST.get('action') == 'resend':
        otp_code = _generate_otp()
        pending['otp_hash'] = make_password(otp_code)
        pending['otp_expires_at'] = (timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat()
        request.session[OTP_SESSION_KEY] = pending
        request.session.modified = True

        try:
            _send_registration_otp(pending['form_data']['email'], otp_code)
        except Exception:
            messages.error(request, 'We could not resend the OTP right now. Please try again.')
        else:
            messages.success(request, 'A fresh OTP has been sent to your email address.')
        return redirect('verify_registration_otp')

    form = OTPVerificationForm(request.POST or None)

    if request.method == 'POST' and request.POST.get('action') != 'resend' and form.is_valid():
        expires_at = datetime.fromisoformat(pending['otp_expires_at'])

        if timezone.now() > expires_at:
            form.add_error('otp', 'This OTP has expired. Click resend to get a new code.')
        elif not check_password(form.cleaned_data['otp'], pending['otp_hash']):
            form.add_error('otp', 'Invalid OTP. Please check your email and try again.')
        else:
            register_form = RegisterForm(pending['form_data'])

            if not register_form.is_valid():
                _clear_pending_registration(request)
                messages.error(request, 'Your signup data changed or expired. Please register again.')
                return redirect('register')

            user = register_form.save()
            user.role = 'staff'
            user.save(update_fields=['role'])

            staff_group, _ = Group.objects.get_or_create(name='Staff')
            user.groups.add(staff_group)

            _clear_pending_registration(request)
            messages.success(request, 'Email verified successfully. You can now log in.')
            return redirect('login')

    return render(request, 'verify_otp.html', {
        'form': form,
        'pending_email': pending['form_data']['email'],
        'otp_expiry_minutes': OTP_EXPIRY_MINUTES,
    })
