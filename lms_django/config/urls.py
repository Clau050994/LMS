from django.contrib import admin
from django.urls import path
from books import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home dashboard
    path("", views.dashboard, name="dashboard"),

    # Dashboards
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/librarian/", views.dashboard_librarian, name="dashboard_librarian"),

    # Authentication
    path("login/", views.RoleBasedLoginView.as_view(template_name="books/dashboard.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    # Librarian + Book functionality
    path("search/", views.search_books, name="search_books"),
    path("borrow/", views.borrow_book, name="borrow_book"),
    path("return/", views.return_book, name="return_book"),




    # Admin: employee and librarian management
    path("register-employee/", views.register_employee, name="register_employee"),
    path("register-client/", views.register_client, name="register_client"),

    # Admin: book inventory management
    path("books/inventory/", views.view_books_admin, name="view_books_admin"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/edit/<str:book_id>/", views.edit_book, name="edit_book"),
    path("books/delete/<str:book_id>/", views.delete_book, name="delete_book"),
    path("books/assigned/", views.assigned_books, name="assigned_books"),


    # Django admin panel
    path("admin/", admin.site.urls),
]
