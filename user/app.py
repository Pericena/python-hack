from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# ==========================
# 🔁 FUNCIONES DE ARCHIVO
# ==========================
def cargar_usuarios():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def guardar_usuarios(lista):
    
    with open(DATA_FILE, 'w') as f:
        json.dump(lista, f, indent=2)

# ==========================
# 🌐 ENDPOINTS
# ==========================

@app.route('/')
def inicio():
    return "¡Bienvenido a la API de usuarios!"

# GET: Listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = cargar_usuarios()
    return jsonify(usuarios)

# GET: Obtener usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuarios = cargar_usuarios()
    for usuario in usuarios:
        if usuario['id'] == id:
            return jsonify(usuario)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# POST: Crear nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    usuarios = cargar_usuarios()
    nuevo_usuario = request.get_json()
    nuevo_usuario['id'] = len(usuarios) + 1
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    return jsonify(nuevo_usuario), 201

# DELETE: Eliminar usuario por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuarios = cargar_usuarios()
    usuarios = [u for u in usuarios if u['id'] != id]
    guardar_usuarios(usuarios)
    return jsonify({'mensaje': f'Usuario {id} eliminado'})

# PUT: Modificar usuario por ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuarios = cargar_usuarios()
    datos_actualizados = request.get_json()
    for i, usuario in enumerate(usuarios):
        if usuario['id'] == id:
            usuarios[i].update(datos_actualizados)
            guardar_usuarios(usuarios)
            return jsonify(usuarios[i])
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# ==========================
# 🚀 INICIO DE LA APP
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
