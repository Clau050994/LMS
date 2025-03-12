"""
URL configuration for lms_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from books import views

urlpatterns = [
    # Homepage - Dashboard Redirects Based on User Role
    path("", views.dashboard, name="dashboard"),

    # Authentication (Login & Logout)
    path("login/", auth_views.LoginView.as_view(template_name="books/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Admin & Librarian Functionalities
    path("register/", views.register, name="register"),  # Register new users
    path("search/", views.search_books, name="search_books"),  # Search books
    path("borrow/", views.borrow_book, name="borrow_book"),  # Borrow a book
    path("return/", views.return_book, name="return_book"),  # Return a book
    path("register-client/", views.register_client, name="register_client"),  # Register new client
]
