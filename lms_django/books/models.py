from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("librarian", "Librarian"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="librarian")

    # Fix reverse accessor clashes
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="librarian")

