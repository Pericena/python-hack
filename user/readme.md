

Listar usuarios

curl http://127.0.0.1:5000/usuarios


Crear usuario
curl -X POST http://127.0.0.1:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Luishiño", "email": "luishino@example.com"}



