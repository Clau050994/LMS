from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from books.decorators import role_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
from .forms import EmployeeRegistrationForm
from django.utils.timezone import make_aware
from datetime import datetime
from pytz import timezone
from django.contrib import messages

import requests
from datetime import datetime
from django.utils.timezone import now, localtime, make_aware, utc
from django.utils.dateformat import format as django_format

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Firebase setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CRED_PATH = os.path.join(BASE_DIR, '..', 'lms_backend', 'firebase_config.json')
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Flask API
FLASK_API_URL = "http://127.0.0.1:5000/books"


# Main dashboard
def dashboard(request):
    return render(request, "books/dashboard.html")

@login_required
@role_required(['admin'])
def dashboard_admin(request):
    return render(request, 'books/dashboard_admin.html')

@login_required
@role_required(['admin', 'librarian'])
def dashboard_librarian(request):
    return render(request, 'books/dashboard_librarian.html')


class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if hasattr(user, "role"):
            print(f"User role: {user.role}")
            if user.role == "admin":
                return "/dashboard/admin/"
            elif user.role == "librarian":
                return "/dashboard/librarian/"
            else:
                messages.error(self.request, "Unknown role. Contact support.")
                return "/login/"
        else:
            messages.error(self.request, "User has no role assigned.")
            return "/login/"


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


@login_required
def search_books(request):
    query = request.GET.get('query', '').strip().lower()
    try:
        response = requests.get(FLASK_API_URL)
        response.raise_for_status()
        books = response.json()
    except requests.RequestException as e:
        print("Error fetching books:", e)
        books = []

    if query:
        books = [book for book in books if query in book['title'].lower()]

    return render(request, 'books/search_books.html', {
        'books': books,
        'query': request.GET.get('query', '')
    })


@login_required
@role_required(['admin', 'librarian'])
def borrow_book(request):
    books_ref = db.collection("books").where("available", "==", True)
    clients_ref = db.collection("clients")
    available_books = [doc.to_dict() | {"id": doc.id} for doc in books_ref.stream()]
    clients = [doc.to_dict() | {"id": doc.id} for doc in clients_ref.stream()]

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        client_id = request.POST.get("client_id")

        if book_id and client_id:
            client = db.collection("clients").document(client_id).get().to_dict()
            full_name = client.get("full_name", "Unknown")

            db.collection("books").document(book_id).update({
                "available": False,
                "rented_by": full_name
            })

            db.collection("rentals").add({
                "book_id": book_id,
                "client_id": client_id,
                "rented_on": datetime.utcnow()
            })

            return redirect("dashboard_librarian")

    return render(request, "books/borrow_book.html", {
        "books": available_books,
        "clients": clients
    })


@login_required
def return_book(request):
    if request.method == "POST":
        rental_id = request.POST.get("rental_id")
        book_id = request.POST.get("book_id")

        # Update book status
        try:
            book_ref = db.collection("books").document(book_id)
            book_doc = book_ref.get()
            if book_doc.exists:
                book_ref.update({
                    "available": True,
                    "rented_by": ""
                })
            else:
                print(f"Book with ID {book_id} does not exist.")
        except Exception as e:
            print("Error updating book:", e)

        # Delete rental record
        try:
            db.collection("rentals").document(rental_id).delete()
        except Exception as e:
            print("Error deleting rental:", e)

        return redirect("return_book")

    # Handle GET: show current rentals
    rentals_ref = db.collection("rentals").stream()
    rentals = []

    for doc in rentals_ref:
        rental = doc.to_dict()
        rental_id = doc.id

        client_data = {"full_name": "Unknown", "email": "Unknown"}
        client_id = rental.get("client_id")
        if client_id:
            client_doc = db.collection("clients").document(client_id).get()
            if client_doc.exists:
                client_data = client_doc.to_dict()

        book_data = {"title": "Unknown"}
        book_id = rental.get("book_id")
        if book_id:
            book_doc = db.collection("books").document(book_id).get()
            if book_doc.exists:
                book_data = book_doc.to_dict()

        rented_on = "Unknown"
        rented_on_raw = rental.get("rented_at") or rental.get("rented_on")
        if rented_on_raw:
            try:
                # Firestore returns timestamp as native type or dict
                if hasattr(rented_on_raw, 'timestamp'):
                    dt = rented_on_raw
                elif isinstance(rented_on_raw, dict) and 'seconds' in rented_on_raw:
                    dt = datetime.fromtimestamp(rented_on_raw['seconds'], tz=utc)
                else:
                    dt = rented_on_raw

                rented_on = django_format(localtime(dt), "F j, Y, g:i A")
            except Exception as e:
                print("Date parse error:", e)
                rented_on = str(rented_on_raw)

        rentals.append({
            "rental_id": rental_id,
            "book_id": book_id,
            "client_name": client_data.get("full_name", "Unknown"),
            "client_email": client_data.get("email", "Unknown"),
            "book_title": book_data.get("title", "Unknown"),
            "rented_on": rented_on
        })

    return render(request, "books/return_book.html", {"rentals": rentals})


@login_required
@role_required(['admin', 'librarian'])
def register_client(request):
    if request.method == "POST":
        client_data = {
            "full_name": request.POST.get("username"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "D-Licence": request.POST.get("drivers_license"),
            "created_at": now()
        }
        db.collection("clients").add(client_data)
        return redirect("dashboard_librarian")

    return render(request, "books/register_client.html")


@login_required
@role_required(['admin', 'librarian'])
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'books/register_employee.html', {'form': form})


@login_required
@role_required(['admin'])
def view_books_admin(request):
    books_ref = db.collection("books")
    books = [doc.to_dict() | {"id": doc.id} for doc in books_ref.stream()]
    total_books = len(books)
    return render(request, "books/view_books_admin.html", {"books": books, "total_books": total_books})


@login_required
@role_required(['admin'])
def add_book(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "genre": request.POST.get("genre"),
            "isbn": request.POST.get("isbn"),
            "available": True,
            "rented_by": ""
        }
        db.collection("books").add(data)
        return redirect("view_books_admin")
    return render(request, "books/add_book.html")


@login_required
@role_required(['admin'])
def edit_book(request, book_id):
    book_ref = db.collection("books").document(book_id)
    book = book_ref.get().to_dict()

    if request.method == "POST":
        updated = {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "genre": request.POST.get("genre")
        }
        book_ref.update(updated)
        return redirect("view_books_admin")

    return render(request, "books/edit_book.html", {"book": book, "book_id": book_id})


@login_required
@role_required(['admin'])
def delete_book(request, book_id):
    db.collection("books").document(book_id).delete()
    return redirect("view_books_admin")


def logout(request):
    auth_logout(request)
    return redirect("login")
