import secrets

from flask import Blueprint, jsonify, request
from db import get_connection
from ..validators.qr import generar_qr

# Capacidad máxima de reservas por franja horaria
MAX_RESERVAS_POR_FRANJA = 10

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})

@reservas_bp.route('/<int:id_reserva>', methods=['GET'])
def get_reserva(id_reserva):
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})

@reservas_bp.route('/', methods=['POST'])
def crear_reserva():
    data = request.json
    email = data.get("email")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    fecha = data["fecha"]
    hora = data["hora"]
    cantidad_personas = data["cantidad_personas"]

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # verificar disponibilidad
        cursor.execute("""
            SELECT COUNT(*) FROM reservas 
            WHERE fecha = %s AND hora = %s AND estado != 'cancelada'
        """, (fecha, hora))
        resultado = cursor.fetchone()
        total_reservas = resultado[0] if resultado is not None else 0

        if total_reservas >= MAX_RESERVAS_POR_FRANJA:
            return jsonify({"mensaje": "No hay disponibilidad para esa fecha y hora"}), 400

        token_cancelacion = secrets.token_urlsafe(32)

        cursor.execute(
            """INSERT INTO reservas 
            (nombre, email, telefono, fecha, hora, cantidad_personas, token_cancelacion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (nombre, email, telefono, fecha, hora, cantidad_personas, token_cancelacion)
        )

        id_reserva = cursor.lastrowid

        ruta_qr = generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion)
        cursor.execute(
            "UPDATE reservas SET qr_code = %s WHERE id_reserva = %s",
            (ruta_qr, id_reserva)
        )

        enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token_cancelacion, id_reserva)

        conn.commit()
        return jsonify({"mensaje": "Reserva creada correctamente"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al crear la reserva", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@reservas_bp.route('/<int:id_reserva>', methods=['PUT'])
def modificar_reserva(id_reserva):
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})