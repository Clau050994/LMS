from flask import Flask, jsonify
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.borrow_routes import borrow_bp
from routes.return_routes import return_bp
from routes.clients_route import client_bp
from routes.rental_routes import rental_bp
from routes.rental_routes import rental_bp

import sys
import os

# Ensure the current folder is in the import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(borrow_bp, url_prefix='/borrow')
app.register_blueprint(return_bp, url_prefix="/api")
app.register_blueprint(client_bp, url_prefix="/api")
app.register_blueprint(rental_bp, url_prefix="/api")


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    app.run(debug=True)
