from flask import Blueprint, request, jsonify
from models.rentals_model import return_book

return_bp = Blueprint('return_bp', __name__)

@return_bp.route('/', methods=['POST'])
def handle_return():
    data = request.json
    book_id = data.get('book_id')
    client_id = data.get('client_id')
    return jsonify(return_book(book_id, client_id))
