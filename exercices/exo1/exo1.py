# ## Exercice 1: Hello World Multilingue

# **Énoncé**:
# Créez une application Flask avec une route `/hello/<language>` qui retourne un message "Hello" dans la langue spécifiée.

# Exemple d'usage:
# ```bash
# curl http://localhost:5000/hello/english
# # {"message": "Hello!", "language": "english"}

# curl http://localhost:5000/hello/french
# # {"message": "Bonjour!", "language": "french"}
# ```

from flask import Flask, request, jsonify, Blueprint

app = Flask(__name__)

GREETINGS = {
    "french": "Bonjour!",
    "english": "Hello!"
}

@app.route('/hello/<language>', methods= ['GET'])
def hello(language):
    """
    Hello endpoint with optional language parameter

    Args:
        language (str, optional): Language to greet. 

    Returns:
        dict: JSON response with greeting

    Examples:
        GET /hello → {"message": "Hello, english!"}
        GET /hello?language=french → {"message": "Bonjour, french!"}
    """
    lang = language.lower()

    if lang not in GREETINGS :
        return jsonify({
            "success" : False,
            "error": f"Language {language} not found"
        }), 404
    
    return jsonify({
        "message" : GREETINGS[lang],
        "language": lang
    })

if __name__ == '__main__' : 
    app.run(debug= True, port= 5000)
