from flask import Blueprint, request, jsonify
from db import get_connection


auth_bp = Blueprint("auth", __name__)


#para que el administrador pueda autenticarse y entrar con el rol que le permite hacer cambios en la página web
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data["usuario"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM login WHERE usuario = %s AND contraseña = %s",
        (usuario, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return {"mensaje": "Credenciales inválidas"}, 401

    if user[3] == "administrador":
        return {"mensaje": "Login correcto", "rol": "administrador"}, 200
    else:
        return {"mensaje": "Login correcto", "rol": "usuario"}, 200  
    