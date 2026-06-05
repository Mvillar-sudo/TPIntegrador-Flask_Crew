from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from db import execute_db, query_db
auth_bp = Blueprint("auth", __name__)


#para que el administrador pueda autenticarse y entrar con el rol que le permite hacer cambios en la página web
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "usuario" not in data or "password" not in data:
       return {"mensaje": "Faltan campos"}, 400

    usuario = data["usuario"]
    password = data["password"]
    query = "SELECT * FROM login WHERE usuario = %s AND password = %s"
    args = (usuario, password)
    query_db(query, args)

    if not user:
        return {"mensaje": "Credenciales inválidas"}, 401
    
    if not check_password_hash(user["contraseña"], password):
        return {"mensaje": "Credenciales inválidas"}, 401

    if user["rol"] == "administrador":
        return {"mensaje": "Login correcto", "rol": "administrador"}, 200
    else:
        return {"mensaje": "Login correcto", "rol": "usuario"}, 200  
    

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or "usuario" not in data or "password" not in data:
        return {"mensaje": "Faltan campos"}, 400

    usuario = data["usuario"]
    password = data["password"]
    rol = "usuario"
    query = "INSERT INTO login (usuario, password, rol) VALUES (%s, %s, %s)",
    args = (usuario, password, rol)

    password_hash = generate_password_hash(password)

    execute_db(query, args)

    return {"mensaje": "Usuario creado correctamente"}, 201    