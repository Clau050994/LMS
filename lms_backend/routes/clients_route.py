from flask import Blueprint, jsonify
from models.clients_model import get_clients


client_bp = Blueprint('client_bp', __name__)

@client_bp.route("/clients", methods=["GET"])
def list_clients():
    return jsonify(get_clients())
