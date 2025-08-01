from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

ARCHIVO_JSON = 'productos.json'

# Leer los productos
def leer_productos():
    with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

# Guardar los productos
def guardar_productos(productos):
    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2)

# Estado temporal de cada usuario (en memoria para simplicidad)
estado_usuario = {}

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data['mensaje']
    usuario_id = 'usuario_1'  # Simulamos un solo usuario para este ejemplo

    if usuario_id not in estado_usuario:
        estado_usuario[usuario_id] = {"paso": 1}

    paso = estado_usuario[usuario_id]["paso"]

    if paso == 1:
        estado_usuario[usuario_id]["nombre"] = mensaje
        estado_usuario[usuario_id]["paso"] = 2
        return jsonify({"respuesta": "¿Cuál es el precio del producto?"})

    elif paso == 2:
        try:
            precio = float(mensaje)
            productos = leer_productos()
            nuevo = {
                "id": productos[-1]["id"] + 1 if productos else 1,
                "nombre": estado_usuario[usuario_id]["nombre"],
                "precio": precio
            }
            productos.append(nuevo)
            guardar_productos(productos)
            estado_usuario[usuario_id] = {"paso": 1}  # Reiniciamos
            return jsonify({"respuesta": f"✅ Producto '{nuevo['nombre']}' guardado con éxito. ¿Quieres agregar otro producto? Escribe el nombre."})
        except ValueError:
            return jsonify({"respuesta": "⚠️ El precio debe ser un número. Intenta de nuevo."})

    return jsonify({"respuesta": "Algo salió mal. Escribe el nombre del producto para comenzar."})

if __name__ == '__main__':
    app.run(debug=True)
