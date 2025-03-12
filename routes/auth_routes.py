from flask import Blueprint, request, jsonify
import bcrypt
from models.user_model import add_user, get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    user = add_user(data['email'], hashed_pw)
    return jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = get_user(data['email'])
    if user and bcrypt.checkpw(data['password'].encode(), user['password'].encode()):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401
