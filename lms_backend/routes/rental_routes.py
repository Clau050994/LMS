from flask import Blueprint, request, jsonify
from models.rentals_model import create_rental, get_active_rentals, return_book
from models.clients_model import get_clients  # ✅ Correct path
from models.book_model import get_books 


# ✅ Define blueprint
rental_bp = Blueprint('rental_bp', __name__)

# GET all active rentals
@rental_bp.route('/rentals', methods=['GET'])
def list_rentals():
    return jsonify(get_active_rentals())

# POST: Rent a book
@rental_bp.route('/rentals', methods=['POST'])
def rent_book():
    data = request.json
    book_id = data.get("book_id")
    client_id = data.get("client_id")
    rental_days = data.get("rental_days", 14)

    if not book_id or not client_id:
        return jsonify({"error": "Missing book_id or client_id"}), 400

    rental = create_rental(book_id, client_id, rental_days)
    return jsonify(rental), 201

# POST: Return a book
@rental_bp.route('/rentals/return', methods=['POST'])
def return_rented_book():
    data = request.json
    book_id = data.get("book_id")
    client_id = data.get("client_id")

    if not book_id or not client_id:
        return jsonify({"error": "Missing book_id or client_id"}), 400

    return jsonify(return_book(book_id, client_id))

@rental_bp.route('/assigned-books', methods=['GET'])
def get_assigned_books():
    rentals = get_active_rentals()
    books = {book['id']: book for book in get_books()}
    clients = {client['id']: client for client in get_clients()}

    enriched = []
    for rental in rentals:
        book_id = rental.get("book_id")
        client_id = rental.get("client_id")
        enriched.append({
            "book_title": books.get(book_id, {}).get("title", "Unknown"),
            "client_name": clients.get(client_id, {}).get("full_name", "Unknown"),
            "due_date": rental.get("due_date", "N/A")
        })

    return jsonify(enriched)
