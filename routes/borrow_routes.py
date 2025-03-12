from flask import Blueprint, request, jsonify
from models.book_model import borrow_book, get_borrowed_books


borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('/', methods=['POST'])
def borrow():
    """Borrow a book"""
    data = request.json
    return jsonify(borrow_book(data['book_id'], data['user_id']))

@borrow_bp.route('/', methods=['GET'])
def borrowed_books():
    """Retrieve all borrowed books"""
    return jsonify(get_borrowed_books())