from config import db

# Test Firebase connection
def test_firestore():
    doc_ref = db.collection("test").document("sample")
    doc_ref.set({"message": "Hello, Firebase!"})
    print("🔥 Firestore is working! Check your Firebase console.")

test_firestore()
