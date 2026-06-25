import secrets
from flask import Blueprint, jsonify, request
from db import get_db
from config import MAX_RESERVAS_POR_FRANJA
from validators.qr import generar_qr
from validators.email import enviar_email_reserva
from services.reservas_service import obtener_reserva_service, listar_reservas_service, crear_reserva_service, cancelar_por_token_service, cancelar_reserva_service, validar_qr_service
from auth_decorators import admin_required

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
        return jsonify(resultado["mensaje"]), resultado["status"]
    except Exception as e:
        return jsonify({"mensaje": "Error al crear la reserva", "error": str(e)}), 500

@reservas_bp.route('/cancelar/<string:token>', methods=['GET'])
def cancelar_por_token(token):
    try:
        resultado = cancelar_por_token_service(token)
        return jsonify(resultado["mensaje"]), resultado["status"]
    except Exception as e:
        return jsonify({"mensaje": "Error al cancelar la reserva", "error": str(e)}), 500

        
@reservas_bp.route('/<int:id_reserva>/cancelar', methods=['PATCH'])
def cancelar_reserva(id_reserva):
    try:
        resultado = cancelar_reserva_service(id_reserva)
        return jsonify(resultado["mensaje"]), resultado["status"]
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

        if resultado["status"] == "no_encontrada":
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
        elif resultado["status"] == "cancelada":
            return jsonify({"mensaje": "La reserva ha sido cancelada"}), 400
        elif resultado["status"] == "qr_invalido":
            return jsonify({"mensaje": "QR inválido, acceso denegado"}), 400
        else:
            return jsonify({"mensaje": "QR válido, acceso permitido"}), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al validar el QR", "error": str(e)}), 500

@reservas_bp.route('/disponibilidad', methods=['GET'])
def verificar_disponibilidad():
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       SELECT COUNT(*) FROM reservas
                       WHERE fecha = %s AND hora = %s AND estado != 'cancelada'
                       """, (fecha, hora)
                       )
        resultado = cursor.fetchone()
        total_reservas = resultado[0] if resultado is not None else 0
        disponibilidad = total_reservas < MAX_RESERVAS_POR_FRANJA
        return jsonify({"disponibilidad": disponibilidad, "reservas_actuales": total_reservas})
    except Exception as e:
        return jsonify({"mensaje": "Error al consultar la disponibilidad"}), 400
    finally:
        cursor.close()