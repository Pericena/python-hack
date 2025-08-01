from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

archivo = 'data/productos.json'

# Función para leer productos desde el archivo
def leer_productos():
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para guardar productos en el archivo
def guardar_productos(productos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2)

# Ruta para mostrar el HTML
@app.route('/')
def index():
    return render_template('productos.html')

# Ruta para obtener productos en formato JSON
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    return jsonify(leer_productos())

# Ruta para agregar un nuevo producto desde HTML
@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    productos = leer_productos()
    nuevo = request.get_json()
    nuevo["id"] = productos[-1]["id"] + 1 if productos else 1
    productos.append(nuevo)
    guardar_productos(productos)
    return jsonify({"mensaje": "Producto agregado correctamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)
