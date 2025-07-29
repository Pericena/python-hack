from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Cargar respuestas desde JSON
with open("bot.json", "r", encoding="utf-8") as file:
    respuestas = json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower()

    respuesta = respuestas.get(mensaje, respuestas["default"])
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)
