import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase Credentials
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

# Database Reference
db = firestore.client()
