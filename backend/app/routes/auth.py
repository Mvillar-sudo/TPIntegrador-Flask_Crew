from flask import Blueprint, request, jsonify, session
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

    session["usuario"] = user["usuario"]
    return jsonify({"mensaje": "Login exitoso"}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    if "usuario" not in session:
        return jsonify({"mensaje": "No hay sesión activa"}), 401
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    if "usuario" not in session:
        return jsonify({"mensaje": "No hay sesión activa"}), 401
    data = request.json

    error, mensaje = validar_login(data)
    if error:
        return {"mensaje": mensaje}, 400

    mensaje = post_register(data)
    return jsonify({"mensaje": mensaje}), 201