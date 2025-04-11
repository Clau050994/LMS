from django.contrib import admin
from django.urls import path
from books import views
from books.views import RoleBasedLoginView  # Custom login view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main landing page (for guests/employees before logging in)
    path("", views.dashboard, name="dashboard"),

    # Role-based dashboards
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/librarian/", views.dashboard_librarian, name="dashboard_librarian"),

    # Django admin panel
    path("admin/", admin.site.urls),

    # Auth
    path("login/", RoleBasedLoginView.as_view(template_name="books/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Functional routes for librarians
    path("register/", views.register, name="register"),
    path("search/", views.search_books, name="search_books"),
    path("borrow/", views.borrow_book, name="borrow_book"),
    path("return/", views.return_book, name="return_book"),
    path("register-client/", views.register_client, name="register_client"),
]
