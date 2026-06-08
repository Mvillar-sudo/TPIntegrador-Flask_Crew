from flask import Blueprint, request, jsonify
from services import post_register, post_login
from validators import validar_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    error, mensaje = validar_login(data)

    if error:
        return jsonify({"mensaje": mensaje}), 400

    user = post_login(data)
    if not user:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

    return jsonify({"mensaje": "Login exitoso",
                    "usuario": user["usuario"]}), 200
                    
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    error, mensaje = validar_login(data)
    if error:
        return {"mensaje": mensaje}, 400

    mensaje = post_register(data)
    return jsonify({"mensaje": mensaje}), 201