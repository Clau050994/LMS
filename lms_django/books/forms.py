from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    pass  # Uses Django's authentication

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "role", "password1", "password2"]
