from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class EmployeeRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("librarian", "Librarian"),
        ("admin", "Admin"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
