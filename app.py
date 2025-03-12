from flask import Flask, jsonify
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.borrow_routes import borrow_bp

app = Flask(__name__)

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(borrow_bp, url_prefix='/borrow')

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    app.run(debug=True)
