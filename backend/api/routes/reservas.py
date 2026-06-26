from flask import Blueprint, jsonify, request
from ..services.reservas_service import (
    obtener_reserva_service,
    listar_reservas_service,
    crear_reserva_service,
    cancelar_por_token_service,
    cancelar_reserva_service,
    validar_qr_service,
    verificar_disponibilidad_service
)
from ..auth_decorators import admin_required

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@reservas_bp.route('/<int:id_reserva>', methods=['GET'])
@admin_required
def detalle_de_una_reserva(id_reserva):
    try:
        reserva = obtener_reserva_service(id_reserva)
        if reserva:
            return jsonify(reserva)
        else:
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la reserva", "error": str(e)}), 500

@reservas_bp.route('/', methods=['GET'])
@admin_required
def listar_todas_las_reservas():
    try:
        reservas = listar_reservas_service()
        return jsonify(reservas)
    except Exception as e:
        return jsonify({"mensaje": "Error al listar las reservas", "error": str(e)}), 500


@reservas_bp.route('/', methods=['POST'])
def crear_reserva():
    data = request.json
    try:
        resultado = crear_reserva_service(data)
        if resultado["estado"] == "creada":
            return jsonify(resultado["mensaje"]), 201
        return jsonify(resultado["mensaje"]), 400
    except Exception as e:
        return jsonify({"mensaje": "Error al crear la reserva", "error": str(e)}), 500

@reservas_bp.route('/cancelar/<string:token>', methods=['GET'])
def cancelar_por_token(token):
    try:
        resultado = cancelar_por_token_service(token)
        if resultado["estado"] == "cancelada":
            return jsonify(resultado["mensaje"]), 200
        return jsonify(resultado["mensaje"]), 400
    except Exception as e:
        return jsonify({"mensaje": "Error al cancelar la reserva", "error": str(e)}), 500

        
@reservas_bp.route('/<int:id_reserva>/cancelar', methods=['PATCH'])
@admin_required
def cancelar_reserva(id_reserva):
    try:
        resultado = cancelar_reserva_service(id_reserva)
        if resultado["estado"] == "cancelada":
            return jsonify(resultado["mensaje"]), 200
        if resultado["estado"] == "no_encontrada":
            return jsonify(resultado["mensaje"]), 404
        return jsonify(resultado["mensaje"]), 400
    except Exception as e:
        return jsonify({"mensaje": "Error al cancelar la reserva", "error": str(e)}), 500
        


@reservas_bp.route('/validar-qr', methods=['POST'])
@admin_required
def validar_qr():
    data = request.json
    id_reserva = data.get("id_reserva")
    qr_code = data.get("qr_code")

    try:
        resultado = validar_qr_service(id_reserva, qr_code)

        if resultado["estado"] == "no_encontrada":
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
        elif resultado["estado"] == "cancelada":
            return jsonify({"mensaje": "La reserva ha sido cancelada"}), 400
        elif resultado["estado"] == "validada":
            return jsonify({"mensaje": "La reserva ha sido validada anteriormente"}), 400
        elif resultado["estado"] == "qr_invalido":
            return jsonify({"mensaje": "QR inválido, acceso denegado"}), 400
        else:
            return jsonify({"mensaje": "QR válido, acceso permitido"}), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al validar el QR", "error": str(e)}), 500


@reservas_bp.route('/disponibilidad', methods=['GET'])
def verificar_disponibilidad():
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")

    if not fecha or not hora:
        return jsonify({"mensaje": "Faltan parámetros requeridos: fecha y hora"}), 400

    try:
        resultado = verificar_disponibilidad_service(fecha, hora)

        return jsonify(resultado), 200

    except Exception:
        return jsonify({"mensaje": "Error al procesar la solicitud de disponibilidad"}), 500
