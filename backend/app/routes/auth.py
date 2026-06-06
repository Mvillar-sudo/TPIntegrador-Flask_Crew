from flask import Blueprint, request, jsonify
from ..db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


#para que el administrador pueda autenticarse y entrar con el rol que le permite hacer cambios en la página web
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "usuario" not in data or "password" not in data:
       return {"mensaje": "Faltan campos"}, 400

    usuario = data["usuario"]
    password = data["password"]

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM login WHERE usuario = %s",
        (usuario,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

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

    password_hash = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO login (usuario, contraseña, rol) VALUES (%s, %s, %s)",
        (usuario, password_hash, rol)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario creado correctamente"}, 201    
