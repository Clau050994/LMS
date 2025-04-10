from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from books import views
from django.shortcuts import render


urlpatterns = [
    # Redirect both root and /dashboard/ to the same view
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard),  
    path("admin/", admin.site.urls),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="books/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Functional Routes
    path("register/", views.register, name="register"),
    path("search/", views.search_books, name="search_books"),
    path("borrow/", views.borrow_book, name="borrow_book"),
    path("return/", views.return_book, name="return_book"),
    path("register-client/", views.register_client, name="register_client"),
]
