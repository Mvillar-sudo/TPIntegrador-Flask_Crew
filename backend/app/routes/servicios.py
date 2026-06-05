from flask import Blueprint, jsonify, request

from ..services.servicios_service import (
    obtener_servicios,
    obtener_servicio_id,
    crear_servicio_db,
    actualizar_servicio_db,
    eliminar_servicio_db
)

from ..validators.servicios_validator import validar_servicio


servicios_bp = Blueprint('servicios',__name__,url_prefix='/api/servicios')

# get todos
@servicios_bp.route('/', methods=['GET'])
def get_servicios():
    try:
        servicios = obtener_servicios()
        return jsonify(servicios), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# get por id
@servicios_bp.route('/<int:id_servicio>', methods=['GET'])
def get_servicio(id_servicio):
    try:
        servicio = obtener_servicio_id(id_servicio)

        if not servicio:
            return jsonify({
                "error": "Servicio no encontrado"
            }), 404

        return jsonify(servicio), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# POST
@servicios_bp.route('/', methods=['POST'])
def crear_servicio():
    try:
        data = request.get_json()

        error = validar_servicio(data)

        if error:
            return jsonify({
                "error": error
            }), 400

        crear_servicio_db(data)

        return jsonify({
            "mensaje": "Servicio creado correctamente"
        }), 201

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# patch
@servicios_bp.route('/<int:id_servicio>', methods=['PATCH'])
def actualizar_servicio(id_servicio):
    try:
        data = request.get_json()

        error = validar_servicio(
            data,
            es_actualizacion=True
        )

        if error:
            return jsonify({
                "error": error
            }), 400

        servicio = obtener_servicio_id(id_servicio)

        if not servicio:
            return jsonify({
                "error": "Servicio no encontrado"
            }), 404

        actualizar_servicio_db(
            id_servicio,
            data
        )

        return jsonify({
            "mensaje": "Servicio actualizado correctamente"
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


# delete
@servicios_bp.route('/<int:id_servicio>', methods=['DELETE'])
def eliminar_servicio(id_servicio):
    try:
        filas = eliminar_servicio_db(id_servicio)

        if filas == 0:
            return jsonify({
                "error": "Servicio no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Servicio eliminado correctamente"
        }), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500