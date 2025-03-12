from config import db

def add_user(email, password):
    user_ref = db.collection("users").document(email)
    user_ref.set({"email": email, "password": password})
    return {"email": email}

def get_user(email):
    user_ref = db.collection("users").document(email).get()
    return user_ref.to_dict() if user_ref.exists else None
