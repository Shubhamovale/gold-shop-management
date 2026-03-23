from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a strong password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat your password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'staff'
        if commit:
            user.save()
        return user


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        label='Email OTP',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'inputmode': 'numeric',
            'autocomplete': 'one-time-code',
        })
    )
