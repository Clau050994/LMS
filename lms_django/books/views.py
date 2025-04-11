from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
import requests
from django.contrib.auth.decorators import login_required
from firebase_admin import firestore

FLASK_API_URL = "http://127.0.0.1:5000/books"

# Main system dashboard (before login)
def dashboard(request):
    return render(request, "books/dashboard.html")

# Role-based dashboards after login
@login_required
def dashboard_admin(request):
    return render(request, "books/dashboard_admin.html")

@login_required
def dashboard_librarian(request):
    return render(request, "books/dashboard_librarian.html")


# Custom LoginView to redirect users by role
class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, "role"):
            if user.role == "admin":
                return "/dashboard/admin/"
            elif user.role == "librarian":
                return "/dashboard/librarian/"
        return super().get_success_url()


# Register a new Django user (employee/librarian)
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "books/register.html", {"form": form})


# Librarian functionality: Search books
@login_required
def search_books(request):
    books = []
    query = request.GET.get('query', '').strip()

    if query:
        db = firestore.client()
        books_ref = db.collection('books')
        # Firestore doesn't support full-text search natively.
        # For demonstration, we'll fetch all books and filter them manually.
        docs = books_ref.stream()
        for doc in docs:
            book = doc.to_dict()
            if query.lower() in book.get('title', '').lower():
                books.append(book)

    return render(request, 'books/search_books.html', {'books': books, 'query': query})

# Librarian functionality: Borrow books
@login_required
def borrow_book(request):
    if request.method == "POST":
        data = {
            "book_id": request.POST.get("book_id"),
            "user_id": request.user.id,
        }
        response = requests.post(f"{FLASK_API_URL}/borrow/", json=data)
        if response.status_code == 200:
            return redirect("dashboard_librarian")
    return render(request, "books/borrow_book.html")


# Librarian functionality: Return books
@login_required
def return_book(request):
    if request.method == "POST":
        data = {"book_id": request.POST.get("book_id")}
        response = requests.post(f"{FLASK_API_URL}/return/", json=data)
        if response.status_code == 200:
            return redirect("dashboard_librarian")
    return render(request, "books/return_book.html")


# Admin-only: Register a new librarian/client
@login_required
def register_client(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "role": "librarian",
        }
        # TODO: Send data to backend or Firebase
        return redirect("dashboard_admin")
    return render(request, "books/register_client.html")
