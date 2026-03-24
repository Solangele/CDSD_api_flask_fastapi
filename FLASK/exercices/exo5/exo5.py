# ## Exercice 5: Calculatrice API

# **Énoncé**:
# Créez une route `/calculate` qui accepte:
# - `operation`: "add", "subtract", "multiply", "divide"
# - `a`: premier nombre
# - `b`: deuxième nombre

# Exemple:
# ```bash
# curl "http://localhost:5000/calculate?operation=add&a=10&b=5"
# # {"operation": "add", "a": 10, "b": 5, "result": 15}

# curl "http://localhost:5000/calculate?operation=divide&a=10&b=0"
# # {"error": "Cannot divide by zero"}
# ```


from flask import Flask, request, jsonify
import re
from datetime import datetime


app = Flask(__name__)

a = 0
b = 0

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0 :
        return None
    return a / b


@app.route('/calculate', methods = ['GET'])
def calculate():
    operation = request.args.get('operation')
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return jsonify({"error": "Les paramètres 'a' et 'b' doivent être des nombres"}), 400

    result = None
    
    if operation == "add":
        result = add(a, b)
    elif operation == "subtract":
        result = subtract(a, b)
    elif operation == "multiply":
        result = multiply(a, b)
    elif operation == "divide":
        result = divide(a, b)
        if result is None:
            return jsonify({"error": "Cannot divide by zero"}), 400
    else:
        return jsonify({"error": "Opération invalide"}), 400

    # 3. Réponse
    return jsonify({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug= True, port= 5000) 