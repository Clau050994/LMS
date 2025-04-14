from config import db

def add_book(title, author, genre, isbn):
    """Add a new book to the Firestore 'books' collection"""
    book_data = {
        "title": title,
        "author": author,
        "genre": genre,
        "isbn": isbn,
        "rented_by": "",     # Empty string means not currently rented
        "available": True    # Available by default
    }
    doc_ref = db.collection("books").add(book_data)
    return {**book_data, "id": doc_ref[1].id}


def get_books():
    """Retrieve all books from Firestore"""
    books = db.collection("books").stream()
    book_list = [{**book.to_dict(), "id": book.id} for book in books]
    return book_list


def update_book(book_id, data):
    """Update book fields"""
    db.collection("books").document(book_id).update(data)
    return {"message": f"Book {book_id} updated successfully"}


def delete_book(book_id):
    """Delete a book document"""
    db.collection("books").document(book_id).delete()
    return {"message": f"Book {book_id} deleted"}


def borrow_book(book_id, client_id):
    """Mark a book as borrowed by setting 'rented_by' and 'available'"""
    db.collection("books").document(book_id).update({
        "rented_by": client_id,
        "available": False
    })
    return {"message": f"Book {book_id} borrowed by {client_id}"}


def return_book(book_id):
    """Mark a book as returned and available again"""
    db.collection("books").document(book_id).update({
        "rented_by": "",
        "available": True
    })
    return {"message": f"Book {book_id} returned successfully"}


def get_borrowed_books():
    """Fetch all currently borrowed books"""
    books = db.collection("books").where("available", "==", False).stream()
    return [{**book.to_dict(), "id": book.id} for book in books]
