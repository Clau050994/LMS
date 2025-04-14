from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if hasattr(user, 'role') and user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("🚫 You do not have permission to access this page.")
        return wrapper
    return decorator
