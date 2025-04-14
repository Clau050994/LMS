from datetime import datetime, timedelta
from config import db

def create_rental(book_id, client_id, rental_days=14):
    """Record a rental with optional due date (default: 14 days)"""
    rented_at = datetime.utcnow()
    due_date = rented_at + timedelta(days=rental_days)
    
    rental_data = {
        "book_id": book_id,
        "client_id": client_id,
        "rented_at": rented_at,
        "due_date": due_date,
        "returned": False
    }
    
    doc_ref = db.collection("rentals").add(rental_data)
    
    # Mark the book as rented in books collection
    db.collection("books").document(book_id).update({
        "available": False,
        "rented_by": client_id
    })

    return {**rental_data, "id": doc_ref[1].id}


def get_active_rentals():
    """Return list of currently active (not returned) rentals"""
    rentals = db.collection("rentals").where("returned", "==", False).stream()
    return [{**r.to_dict(), "id": r.id} for r in rentals]


def mark_rental_returned(rental_id):
    """Mark a rental as returned"""
    db.collection("rentals").document(rental_id).update({
        "returned": True,
        "returned_at": datetime.utcnow()
    })
    return {"message": f"Rental {rental_id} marked as returned"}


def return_book(book_id, client_id):
    """
    Return a book and mark rental as returned.
    """
    # Step 1: Mark the book as available again
    db.collection("books").document(book_id).update({
        "available": True,
        "rented_by": ""
    })

    # Step 2: Mark the latest active rental for that book and client as returned
    rentals = db.collection("rentals")\
        .where("book_id", "==", book_id)\
        .where("client_id", "==", client_id)\
        .where("returned", "==", False)\
        .stream()

    for rental in rentals:
        db.collection("rentals").document(rental.id).update({
            "returned": True,
            "returned_at": datetime.utcnow()
        })

    return {"message": "Book returned successfully"}
