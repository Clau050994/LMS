from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            print("User authenticated:", request.user.is_authenticated)
            print("User:", request.user)
            print("User role:", getattr(request.user, "role", None))
            print("Allowed roles:", allowed_roles)
            if hasattr(request.user, "role") and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator
