from flask import Blueprint, request, jsonify
from services import post_register, post_login, obtener_usuarios, obtener_usuario, eliminar_usuario, actualizar_usuario
from validators import validar_login
from auth_decorators import admin_required
auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    error, mensaje = validar_login(data)

    if error:
        return jsonify({"mensaje": mensaje}), 400

    user = post_login(data)
    if not user:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

    return jsonify({"mensaje": "Login exitoso",
                    "token": user["token"],
                    "usuario": user["usuario"]}), 200


@auth_bp.route("/api/register", methods=["POST"])
@admin_required
def register():
    data = request.json

    error, mensaje = validar_login(data)
    if error:
        return {"mensaje": mensaje}, 400

    try:
        mensaje = post_register(data)
        return jsonify({"mensaje": mensaje}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al registrar: {str(e)}"}), 500 

@auth_bp.route("/api/admin/usuarios", methods=["GET"])
@admin_required
def ver_usuarios_admin():

    usuarios = obtener_usuarios()

    return jsonify(usuarios), 200 

@auth_bp.route('/api/admin/usuarios/<int:id_usuario>', methods=['GET'])
@admin_required
def get_usuario(id_usuario):
    try:
        usuario = obtener_usuario(id_usuario)

        if not usuario:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        return jsonify(usuario), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500 

@auth_bp.route('/api/admin/usuarios/<int:id_usuario>', methods=['PATCH'])
@admin_required
def patch_usuario(id_usuario):
    try:
        data = request.get_json()

        usuario = obtener_usuario(id_usuario)

        if not usuario:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        actualizar_usuario(
            id_usuario,
            data
        )

        return jsonify({
            "mensaje": "Usuario actualizado correctamente"
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/api/admin/usuarios/<int:id_usuario>', methods=['DELETE'])
@admin_required
def borrar_usuario(id_usuario):
    try:
        filas = eliminar_usuario(id_usuario)

        if filas == 0:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Usuario eliminado correctamente"
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500