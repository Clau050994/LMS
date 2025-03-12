from config import db

def add_book(title, author, genre):
    """Add book to Firestore"""
    doc_ref = db.collection("books").add({"title": title, "author": author, "genre": genre})
    return {"id": doc_ref[1].id, "title": title, "author": author, "genre": genre}


def get_books():
    """Retrieve all books from Firestore"""
    books = db.collection("books").stream()
    book_list = [{**book.to_dict(), "id": book.id} for book in books]

    print("📚 Retrieved books:", book_list)
    return book_list

def update_book(book_id, data):
    """Update book details"""
    db.collection("books").document(book_id).update(data)
    return {"message": "Book updated"}

def delete_book(book_id):
    """Delete a book"""
    db.collection("books").document(book_id).delete()
    return {"message": "Book deleted"}
def borrow_book(book_id, user_id):
    """Mark a book as borrowed"""
    book_ref = db.collection("books").document(book_id)
    book_ref.update({"borrowed_by": user_id, "status": "borrowed"})
    return {"message": f"Book {book_id} borrowed by {user_id}"}

def get_borrowed_books():
    """Retrieve all borrowed books"""
    books = db.collection("books").where("status", "==", "borrowed").stream()
    return [{**book.to_dict(), "id": book.id} for book in books]
