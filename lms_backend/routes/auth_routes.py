from flask import Blueprint, request, jsonify, session
import bcrypt
from models.user_model import add_user, get_user, login_user




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
    email = data.get("email")
    password = data.get("password")

    user = login_user(email, password)
    if user:
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        return jsonify({"message": "Login successful", "role": user['role']})
    else:
        return jsonify({"error": "Invalid credentials"}), 401