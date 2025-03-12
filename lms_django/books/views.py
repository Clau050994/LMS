from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import requests

FLASK_API_URL = "http://127.0.0.1:5000/books"

def register(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "books/register.html", {"form": form})

@login_required
def dashboard(request):
    """Handles dashboard for Admin and Librarians"""
    if hasattr(request.user, "role") and request.user.role == "admin":
        return render(request, "books/dashboard_admin.html")
    else:
        return render(request, "books/dashboard_librarian.html")

@login_required
def search_books(request):
    """Search books from the Flask backend"""
    books = []
    if request.method == "POST":
        search_query = request.POST.get("search", "")
        response = requests.get(f"{FLASK_API_URL}?query={search_query}")
        if response.status_code == 200:
            books = response.json()
    return render(request, "books/search_books.html", {"books": books})

@login_required
def borrow_book(request):
    """Borrow a book"""
    if request.method == "POST":
        data = {
            "book_id": request.POST.get("book_id"),
            "user_id": request.user.id,
        }
        response = requests.post(f"{FLASK_API_URL}/borrow/", json=data)
        if response.status_code == 200:
            return redirect("dashboard")
    return render(request, "books/borrow_book.html")

@login_required
def return_book(request):
    """Return a borrowed book"""
    if request.method == "POST":
        data = {"book_id": request.POST.get("book_id")}
        response = requests.post(f"{FLASK_API_URL}/return/", json=data)
        if response.status_code == 200:
            return redirect("dashboard")
    return render(request, "books/return_book.html")

@login_required
def register_client(request):
    """Register a new librarian (Admin only)"""
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "role": "librarian",
        }
        # TODO: Send data to Firebase or Flask backend
        return redirect("dashboard")
    return render(request, "books/register_client.html")
