from flask import Blueprint, request, jsonify
from models.book_model import add_book, update_book, delete_book, get_books

# Define Blueprint for books
book_bp = Blueprint('book', __name__)

@book_bp.route('', methods=['GET'])
def list_books():
    """Retrieve all books from Firestore"""
    return jsonify(get_books())

@book_bp.route('', methods=['POST'])
def create_book():
    """Add a new book"""
    data = request.json
    return jsonify(add_book(data['title'], data['author'], data['genre'])), 201

@book_bp.route('/<id>', methods=['PUT'])
def edit_book(id):
    """Update book details"""
    data = request.json
    return jsonify(update_book(id, data))

@book_bp.route('/<id>', methods=['DELETE'])
def remove_book(id):
    """Delete a book"""
    return jsonify(delete_book(id))
