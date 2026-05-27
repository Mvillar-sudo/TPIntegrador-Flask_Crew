from flask import Blueprint, jsonify, request
from services.resenas_service import (
    obtener_resenas,
    obtener_resena_id,
    crear_resena_db,
    aprobar_resena_db,
    eliminar_resena_db
)
from validators.resena_validator import validar_resena

reseñas_bp = Blueprint('reseñas', __name__, url_prefix='/api/resenas')


# pública (clientes)

@reseñas_bp.route('/', methods=['GET'])
def get_resenas():
    try:
        resenas = obtener_resenas()
        return jsonify(resenas), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@reseñas_bp.route('/<int:id_resena>', methods=['GET'])
def get_resena(id_resena):
    try:
        resena = obtener_resena_id(id_resena)
        if not resena:
            return jsonify({"error": "Reseña no encontrada"}), 404
        return jsonify(resena), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@reseñas_bp.route('/', methods=['POST'])
def crear_resena():
    try:
        data = request.get_json()
        error = validar_resena(data)
        if error:
            return jsonify({"error": error}), 400
        crear_resena_db(data)
        return jsonify({"mensaje": "Reseña creada correctamente"}), 201
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# privada (admin)

@reseñas_bp.route('/<int:id_resena>/aprobar', methods=['PATCH'])
def aprobar_resena(id_resena):
    try:
        filas = aprobar_resena_db(id_resena)
        if filas == 0:
            return jsonify({"error": "Reseña no encontrada"}), 404
        return jsonify({"mensaje": "Reseña aprobada correctamente"}), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@reseñas_bp.route('/<int:id_resena>', methods=['DELETE'])
def eliminar_resena(id_resena):
    try:
        filas = eliminar_resena_db(id_resena)
        if filas == 0:
            return jsonify({"error": "Reseña no encontrada"}), 404
        return jsonify({"mensaje": "Reseña eliminada correctamente"}), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500