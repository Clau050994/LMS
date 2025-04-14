from datetime import datetime
from config import db


def create_client(full_name, email, phone, address="", license_number=""):
    """Add a new client to Firestore"""
    client_data = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "address": address,
        "D-Licence": license_number,
        "created_at": datetime.utcnow()
    }
    doc_ref = db.collection("clients").add(client_data)
    return {**client_data, "id": doc_ref[1].id}

def get_clients():
    """Fetch all clients"""
    clients = db.collection("clients").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in clients]
