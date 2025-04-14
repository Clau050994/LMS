from config import db

def add_user(email, password, role="librarian"):
    user_ref = db.collection("users").document(email)
    user_ref.set({
        "email": email,
        "password": password,
        "role": role
    })
    return {"email": email, "role": role}

def get_user(email):
    user_ref = db.collection("users").document(email).get()
    return user_ref.to_dict() if user_ref.exists else None

def login_user(email, password):
    user = get_user(email)
    if user and user["password"] == password:
        return {"email": email, "role": user.get("role", "librarian")}
    return None
