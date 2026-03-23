# ## Exercice 4: Validation de Formulaire

# **Énoncé**:
# Créez une route `/register` qui accepte un POST avec les champs:
# - `username` (2-20 caractères)
# - `email` (format valide)
# - `password` (minimum 8 caractères)
# - `age` (18-100)

# Retournez une liste d'erreurs si la validation échoue.

# Exemple:
# ```bash
# curl -X POST http://localhost:5000/register \
#   -H "Content-Type: application/json" \
#   -d '{"username": "john", "email": "john@example.com", "password": "secure123", "age": 25}'
# # {"message": "Registration successful", "user": {...}}

# curl -X POST http://localhost:5000/register \
#   -H "Content-Type: application/json" \
#   -d '{"username": "j", "email": "invalid", "password": "short", "age": 15}'
# # {"errors": ["username too short", "invalid email", "password too short", "age must be 18+"]}
# ```


from flask import Flask, request, jsonify
import re
from datetime import datetime


app = Flask(__name__)


users_db = {
    1: {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "password": "hashed_password_123",
        "age": 28,
        "first_name": "Alice",
        "last_name": "Smith",
        "created_at": "2024-01-15"
    }
}

next_user_id = 2

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{2,20}$'


def validate_username(username):
    """
    Validate username (alphanumeric + underscore, 2-20 chars)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required and must be a string"

    username = username.strip()
    if not re.match(USERNAME_PATTERN, username):
        return False, "Username must be 2-20 characters (letters, numbers, underscore)"

    return True, None




def validate_email(email):
    """
    Validate email format

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"

    email = email.strip()
    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"

    if not re.match(EMAIL_PATTERN, email):
        return False, "Invalid email format"

    return True, None


def validate_password(password):
    """
    Validate password strength

    Requirements:
        - At least 8 characters

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    return True, None



def validate_age(age):
    """
    Validate age (must be integer between 13 and 120)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if age is None:
        return False, "Age is required"

    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be an integer"

    if age_int < 18:
        return False, "Must be at least 18 years old"

    if age_int > 100:
        return False, "Age cannot exceed 100"

    return True, None



def check_username_exists(username, exclude_id=None):
    """Check if username already exists"""
    for user in users_db.values():
        if user['username'].lower() == username.lower() and user['id'] != exclude_id:
            return True
    return False




def check_email_exists(email, exclude_id=None):
    """Check if email already exists"""
    for user in users_db.values():
        if user['email'].lower() == email.lower() and user['id'] != exclude_id:
            return True
    return False




@app.route('/api/register', methods=['POST'])
def register():
    """
    POST /api/register
    Register new user with comprehensive validation

    Required fields:
        - username: 2-20 chars, alphanumeric + underscore
        - email: valid email format
        - password: 8+ chars, uppercase, lowercase, digit, special char
        - age: 13-120

    Returns:
        201: User registered successfully
        400: Validation error
        409: Username or email already exists
    """
    global next_user_id

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    # Validate required fields
    required = ['username', 'email', 'password', 'age']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            "success": False,
            "error": "Missing required fields",
            "missing_fields": missing
        }), 400

    # Validate username
    is_valid, error = validate_username(data['username'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "username",
            "error": error
        }), 400

    # Check username doesn't exist
    if check_username_exists(data['username']):
        return jsonify({
            "success": False,
            "field": "username",
            "error": "Username already taken"
        }), 409

    # Validate email
    is_valid, error = validate_email(data['email'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "email",
            "error": error
        }), 400

    # Check email doesn't exist
    if check_email_exists(data['email']):
        return jsonify({
            "success": False,
            "field": "email",
            "error": "Email already registered"
        }), 409

    # Validate password
    is_valid, error = validate_password(data['password'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "password",
            "error": error
        }), 400

    # Validate age
    is_valid, error = validate_age(data['age'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "age",
            "error": error
        }), 400

    # All validations passed - create user
    new_user = {
        "id": next_user_id,
        "username": data['username'],
        "email": data['email'],
        "password": f"hashed_{data['password']}",  # In production, hash the password!
        "age": int(data['age']),
        "first_name": data.get('first_name', ''),
        "last_name": data.get('last_name', ''),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {
            "id": new_user['id'],
            "username": new_user['username'],
            "email": new_user['email'],
            "created_at": new_user['created_at']
        }
    }), 201


if __name__ == '__main__':
    app.run(debug=True)



