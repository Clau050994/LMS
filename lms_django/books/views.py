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
from django.utils.timezone import localtime, now
from django.utils.dateformat import format as django_format
from django.contrib import messages
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
from books import views
from datetime import datetime, timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, timezone
from django.contrib.auth.views import LoginView


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
        return self.request.path

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


def search_books(request):
    query = request.GET.get("query", "").strip()
    books = []

    if query:
        # Fetch from Firebase (internal)
        try:
            docs = db.collection("books").stream()
            for doc in docs:
                data = doc.to_dict()
                if query.lower() in data.get("title", "").lower():
                    books.append({
                        "title": data.get("title", "No Title"),
                        "authors": data.get("author", "Unknown"),
                        "description": data.get("description", "No description available."),
                        "publisher": data.get("publisher", "Unknown"),
                        "published_date": data.get("published_date", "Unknown"),
                        "thumbnail": data.get("thumbnail", ""),
                        "source": "internal",
                        "available": data.get("available", True),
                        "rented_by": data.get("rented_by", "N/A")
                    })
        except Exception as e:
            print("Firebase error:", e)

        # Fetch from Google Books
        try:
            g_response = requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                params={"q": query}
            )
            if g_response.status_code == 200:
                g_books = g_response.json().get("items", [])
                for item in g_books:
                    info = item.get("volumeInfo", {})
                    books.append({
                        "title": info.get("title", "No Title"),
                        "authors": ", ".join(info.get("authors", ["Unknown"])),
                        "description": info.get("description", "No description available."),
                        "publisher": info.get("publisher", "Unknown"),
                        "published_date": info.get("publishedDate", "Unknown"),
                        "thumbnail": info.get("imageLinks", {}).get("thumbnail", ""),
                        "source": "google",
                        "available": True,
                        "rented_by": ""
                    })
        except Exception as e:
            print("Google Books API error:", e)

    return render(request, "books/search_books.html", {
        "books": books,
        "query": query
    })

def borrow_google_book(request):
    if request.method == "POST":
        data = request.POST
        try:
            book_data = {
                "title": data.get("title"),
                "authors": data.get("authors"),
                "publisher": data.get("publisher"),
                "published_date": data.get("published_date"),
                "thumbnail": data.get("thumbnail"),
                "description": data.get("description"),
                "available": False,
                "rented_by": data.get("client_id"),
                "source": "google"
            }

            # Save to Firestore
            book_ref = db.collection("books").add(book_data)

            client_id = data.get("client_id")
            client_ref = db.collection("clients").document(client_id).get()
            client_data = client_ref.to_dict() if client_ref.exists else {}

            db.collection("rentals").add({
                "book_id": book_ref[1].id,
                "client_id": client_id,
                "client_name": client_data.get("name", "Unknown"),
                "email": client_data.get("email", "Unknown"),
                "rented_at": now(),
                "due_date": now() + timedelta(days=14),
                "returned": False
            })

            messages.success(request, f"Book '{data.get('title')}' borrowed successfully.")

        except Exception as e:
            messages.error(request, f"Failed to borrow book: {str(e)}")

        return redirect("search_books")
    return redirect('search_books')

def borrow_internal_book(request):
    if request.method == "POST":
        try:
            book_id = request.POST.get("book_id")
            client_id = request.POST.get("client_id")

            if not book_id or not client_id:
                messages.error(request, "Missing book ID or client ID.")
                return redirect("search_books")

            book_ref = db.collection("books").document(book_id)


            # Fetch the book from Firebase
            book_ref = db.collection("books").document(book_id)
            book_snapshot = book_ref.get()

            if book_snapshot.exists:
                book_data = book_snapshot.to_dict()

                if not book_data.get("available", True):
                    messages.error(request, "This book is already borrowed.")
                    return redirect("search_books")

                # Update the book to mark it as borrowed
                book_ref.update({
                    "available": False,
                    "rented_by": client_id
                })
                messages.success(request, "Book borrowed successfully.")
                # Add to rentals collection
                db.collection("rentals").add({
                    "book_id": book_ref[1].id,
                    "client_id": client_id,
                    "client_name": client_data.get("name", "Unknown"),
                    "email": client_data.get("email", "Unknown"),
                    "rented_at": now(),
                    "due_date": now() + timedelta(days=14),
                    "returned": False
                })
            else:
                messages.error(request, "Book not found.")
        except Exception as e:
            messages.error(request, f"Error borrowing book: {e}")

        return redirect("search_books")
    return redirect("search_books")

@login_required
@role_required(['admin', 'librarian'])
def borrow_book(request):
    clients = []
    books = []

    # Fetch clients and available books
    try:
        clients_ref = db.collection("clients").stream()
        books_ref = db.collection("books").where("available", "==", True).stream()
        clients = [{"id": doc.id, **doc.to_dict()} for doc in clients_ref]
        books = [{"id": doc.id, **doc.to_dict()} for doc in books_ref]
    except Exception as e:
        print("Error fetching clients or books:", e)

    if request.method == "POST":
        client_id = request.POST.get("client_id")
        book_id = request.POST.get("book_id")
        due_date = request.POST.get("due_date")  # ✅ Due date from form input

        if client_id and book_id and due_date:
            try:
                # Step 1: Update the book to mark it as rented
                db.collection("books").document(book_id).update({
                    "available": False,
                    "rented_by": client_id
                })

                # Step 2: Add a rental record with returned set to False
                client_ref = db.collection("clients").document(client_id).get()
                client_data = client_ref.to_dict() if client_ref.exists else {}

                db.collection("rentals").add({
                    "book_id": book_id,
                    "client_id": client_id,
                    "client_name": client_data.get("name", "Unknown"),
                    "email": client_data.get("email", "Unknown"),
                    "rented_at": now(),
                    "due_date": due_date,
                    "returned": False
                })

                messages.success(request, "Book rented successfully!")
                return redirect("borrow_book")

            except Exception as e:
                messages.error(request, f"Rental failed: {str(e)}")
        else:
            messages.error(request, "All fields including due date are required.")

    return render(request, "books/borrow_book.html", {
        "clients": clients,
        "books": books
    })


@login_required
def return_book(request):
    if request.method == "POST":
        rental_id = request.POST.get("rental_id")
        book_id = request.POST.get("book_id")
        print("Rental ID:", rental_id)
        print("Book ID:", book_id)

        # Step 1: Fetch the book from Firestore
        book_ref = db.collection("books").document(book_id)
        book_snapshot = book_ref.get()

        # Check if the book exists
        if not book_snapshot.exists:
            messages.error(request, "Book not found.")
            return redirect('return_book')

        # ✅ Step 1: Update book availability
        try:
            db.collection("books").document(book_id).update({
                "available": True,
                "rented_by": ""
            })
            print("Book availability updated successfully.")
        except Exception as e:
            print("Error updating book:", e)

        # ✅ Step 2: Mark rental as returned
        try:
            db.collection("rentals").document(rental_id).update({
                "returned": True,
                "returned_at": datetime.utcnow()
            })
        except Exception as e:
            print("Error updating rental status:", e)

        return redirect("return_book")

    # 🟡 Step 3: Fetch only active (not yet returned) rentals
    rentals_ref = db.collection("rentals").where("returned", "==", False).stream()
    rentals = []

    for doc in rentals_ref:
        rental = doc.to_dict()
        rental_id = doc.id

        # 🔄 Get client info
        client_data = {"full_name": "Unknown", "email": "Unknown"}
        client_id = rental.get("client_id")
        if client_id:
            client_doc = db.collection("clients").document(str(client_id)).get()
            if client_doc.exists:
                client_data = client_doc.to_dict()

        # 🔄 Get book info (robust handling of DocumentReference or string ID)
        book_data = {"title": "Unknown"}
        book_id = "Unknown"

        book_ref = rental.get("book_id")
        print("DEBUG - book_ref:", book_ref, "type:", type(book_ref))

        try:
            if isinstance(book_ref, firestore.DocumentReference):
                book_doc = book_ref.get()
                book_id = book_ref.id
            elif isinstance(book_ref, str):
                book_doc = db.collection("books").document(book_ref).get()
                book_id = book_ref
            else:
                raise ValueError(f"Unexpected book_ref type: {type(book_ref)}")

            if book_doc.exists:
                book_data = book_doc.to_dict()
        except Exception as e:
            print("Error fetching book data:", e)

        # 📅 Format rental date
        rented_on = "Unknown"
        rented_on_raw = rental.get("rented_at")
        if rented_on_raw:
            try:
                if hasattr(rented_on_raw, 'timestamp'):
                    dt = rented_on_raw
                elif isinstance(rented_on_raw, dict) and 'seconds' in rented_on_raw:
                    dt = datetime.fromtimestamp(rented_on_raw['seconds'], timezone.utc)
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
            "rented_on": rented_on,
            "due_date": rental.get("due_date", "Unknown"),
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
        messages.success(request, "Client registered successfully!")
         # Reload the form page with empty fields after success
        return render(request, "books/register_client.html")

    return render(request, "books/register_client.html")


from django.contrib import messages

@login_required
@role_required(['admin'])
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee registered successfully!")  # ✅ success message
            form = EmployeeRegistrationForm()  # Reset form
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'books/register_employee.html', {'form': form})


def view_books_admin(request):
    books_ref = db.collection("books")
    docs = books_ref.stream()

    books = []
    for doc in docs:
        data = doc.to_dict()

        # Parse and safely extract values
        books.append({
            "id": doc.id,
            "title": data.get("title", "No Title"),
            "author": data.get("author", "Unknown"),
            "genre": data.get("genre", "N/A"),
            "isbn": data.get("isbn", "N/A"),
            "publisher": data.get("publisher", "Unknown"),
            "available": data.get("available", True),
            "rented_by": data.get("rented_by", "")
        })

    return render(request, "books/view_books_admin.html", {
        "books": books,
        "total_books": len(books)
    })


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
        messages.success(request, "Book added successfully!")
        return redirect("add_book")  # Redirect to same page to show success message

    return render(request, "books/add_book.html")

@login_required
@role_required(['admin'])
def edit_book(request, book_id=None):
    book_data = {}

    if book_id:
        # Fetch existing book data
        doc = db.collection("books").document(book_id).get()
        if doc.exists:
            book_data = doc.to_dict()
            book_data["id"] = book_id
        else:
            messages.error(request, "Book not found.")

    if request.method == "POST":
        # Get updated fields
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")

        updates = {}
        if title and title != book_data.get("title"):
            updates["title"] = title
        if author and author != book_data.get("author"):
            updates["author"] = author
        if genre and genre != book_data.get("genre"):
            updates["genre"] = genre

        if updates and book_id:
            db.collection("books").document(book_id).update(updates)
            messages.success(request, "Book updated successfully!")
            book_data.update(updates)
        elif not updates:
            messages.info(request, "No changes were made.")

    return render(request, "books/edit_book.html", {"book_data": book_data})



@login_required
@role_required(['admin'])
def delete_book(request, book_id):
    db.collection("books").document(book_id).delete()
    return redirect("view_books_admin")


def logout(request):
    auth_logout(request)
    messages.info(request, "You Have Logged Out.")
    return redirect('dashboard')


# books/views.py
@login_required
@role_required(['admin', 'librarian'])
def assigned_books(request):
    assigned = []
    try:
        assigned = get_active_rentals()  # Ensure Flask is running
    except Exception as e:
        print("Error fetching assigned books:", e)
        assigned = []

    return render(request, "books/assigned_books.html", {
        "assigned_books": assigned
    })


def get_active_rentals():
    rentals_ref = db.collection("rentals").where("returned", "==", False).stream()
    active_rentals = []

    for doc in rentals_ref:
        rental = doc.to_dict()

        # Fetch client name
        client_name = "Unknown"
        client_id = rental.get("client_id")
        if client_id:
            client_doc = db.collection("clients").document(client_id).get()
            if client_doc.exists:
                client_name = client_doc.to_dict().get("full_name", "Unknown")

        # Fetch book title
        book_title = "Unknown"
        book_id = rental.get("book_id")
        if book_id:
            book_doc = db.collection("books").document(book_id).get()
            if book_doc.exists:
                book_title = book_doc.to_dict().get("title", "Unknown")

        active_rentals.append({
            "client_name": client_name,
            "book_title": book_title,
            "due_date": rental.get("due_date", "Unknown"),
        })

    return active_rentals