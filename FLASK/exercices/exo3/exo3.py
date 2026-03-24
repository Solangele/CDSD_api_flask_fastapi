# ## Exercice 3: Gestion d'une Liste de Livres

# **Énoncé**:
# Créez une API simple pour gérer une liste de livres en mémoire.

# Routes:
# - `GET /books` - Retourner tous les livres
# - `GET /books/<id>` - Retourner un livre par ID
# - `POST /books` - Ajouter un nouveau livre

# Exemple POST:
# ```bash
# curl -X POST http://localhost:5000/books \
#   -H "Content-Type: application/json" \
#   -d '{"title": "1984", "author": "Orwell", "year": 1949}'
# ```


from flask import Flask, request, jsonify

app = Flask(__name__)

books_db = {
    1: {"id" : 1, "title": "1984", "author" : "Orwell", "year": 1949},
    2: {"id" : 2, "title": "Harry Potter à l'école des sorciers", "author" : "J.K. Rowling", "year": 1997},
    3: {"id" : 3, "title": "Orgueil et préjugés", "author" : "Jane Austen", "year": 1813}
}

next_book_id = 4

@app.route('/api/books', methods=['GET'])
def get_all_books():
    """
    GET /api/books
    Returns list of all books
    """
    return jsonify({
        "success": True,
        "data": list(books_db.values()),
        "count": len(books_db)
    }), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_books(book_id):
    """
    GET /api/books/:id
    Returns specific book by ID
    """

    if book_id not in books_db:
        return jsonify({
            "success": False,
            "error": f"User {book_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": books_db[book_id]
    }), 200


@app.route('/api/books', methods=['POST'])
def create_book():
    """
    POST /api/users
    Create new book with JSON body: {"title": "...", "year": "..."}
    """
    global next_book_id

    # Validate JSON
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    # Validate required fields
    if not data.get('title') or not data.get('author') or not data.get('year'):
        return jsonify({
            "success": False,
            "error": "Missing required fields: title, author, year"
        }), 400

    # Check for duplicate title
    for user in books_db.values():
        if user['title'] == data['title']:
            return jsonify({
                "success": False,
                "error": f"Email {data['title']} already exists"
            }), 409

    # Create new book
    new_book = {
        "id": next_book_id,
        "title": data['title'],
        "author": data['author'],
        "year": data['year']
    }
    books_db[next_book_id] = new_book
    next_book_id += 1

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_book
    }), 201

if __name__ == '__main__':
    app.run(debug= True, port= 5000)