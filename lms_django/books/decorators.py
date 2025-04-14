from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if hasattr(user, "role") and user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Access denied: You are not authorized to view this page.")
                return redirect("dashboard")  # fallback or login
        return _wrapped_view
    return decorator
