from flask import Blueprint, request, jsonify
from models.book_model import add_book, update_book, delete_book, get_books
from .decorators import role_required


# ✅ Define the blueprint
book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/', methods=['GET'])
def list_books():
    books = get_books()
    print("📚 Books being returned:", books)  
    return jsonify(books)

@book_bp.route('', methods=['POST'])
def create_book():
    data = request.json
    return jsonify(add_book(data['title'], data['author'], data['genre'])), 201

@book_bp.route('/<id>', methods=['PUT'])
def edit_book(id):
    data = request.json
    return jsonify(update_book(id, data))

@book_bp.route('/<id>', methods=['DELETE'])
def remove_book(id):
    return jsonify(delete_book(id))

@book_bp.route('/admin-dashboard')
@role_required(['admin'])
def admin_dashboard():
    return jsonify({"message": "Welcome Admin"})

@book_bp.route('/librarian-dashboard')
@role_required(['admin', 'librarian'])
def librarian_dashboard():
    return jsonify({"message": "Welcome Librarian or Admin"})
