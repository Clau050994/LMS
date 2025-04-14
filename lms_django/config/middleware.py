from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is trying to access admin but is not staff, block them
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if not request.user.is_staff:
                return redirect(reverse('dashboard_librarian'))  # Or another appropriate page
        return self.get_response(request)
