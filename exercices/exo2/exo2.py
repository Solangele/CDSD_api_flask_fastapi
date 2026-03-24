# ## Exercice 2: Convertisseur de Température

# **Énoncé**:
# Créez une route `/convert/temp` qui accepte deux paramètres query:
# - `value`: la température (nombre)
# - `unit`: "c2f" (Celsius to Fahrenheit) ou "f2c" (Fahrenheit to Celsius)

# Exemple:
# ```bash
# curl "http://localhost:5000/convert/temp?value=25&unit=c2f"
# # {"celsius": 25, "fahrenheit": 77.0}

# curl "http://localhost:5000/convert/temp?value=77&unit=f2c"
# # {"fahrenheit": 77, "celsius": 25.0}
# ```

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/convert/temp', methods=['GET'])
def convert_temp():
    value = request.args.get('value', type=float)
    unit = request.args.get('unit')

    if value is None or unit is None:
        return jsonify({
            "error": "Veuillez fournir 'value' et 'unit'"
        }), 400

    if unit == "c2f":
        result = (value * 1.8) + 32
        return jsonify({
            "celsius": value, 
            "fahrenheit": result
        })
    
    elif unit == "f2c":
        result = (value - 32) / 1.8
        return jsonify({
            "fahrenheit": value, 
            "celsius": result
        })
    
    else:
        return jsonify({
            "error": "Unité invalide. Utilisez 'c2f' ou 'f2c'"
        }), 400

if __name__ == '__main__':
    app.run(debug= True, port= 5000)

