from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # Your custom user model

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )

admin.site.register(User, UserAdmin)

