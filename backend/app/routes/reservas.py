import secrets
from datetime import datetime
from flask import Blueprint, jsonify, request
from db import get_db, query_db, execute_db
from config import MAX_RESERVAS_POR_FRANJA
from validators.qr import generar_qr
from validators.email import enviar_email_reserva

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@reservas_bp.route('/<int:id_reserva>', methods=['GET'])
def detalle_de_una_reserva(id_reserva):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_reserva, nombre, email, telefono, fecha, hora, cantidad_personas, estado, token, qr_code, fecha_creacion FROM reservas WHERE id_reserva = %s" , (id_reserva,))
        resultado = cursor.fetchone()
        print(resultado)  
        print(type(resultado)) 
        if resultado:
            return jsonify({
                "id_reserva": resultado[0],
                "nombre": resultado[1],
                "email": resultado[2],
                "telefono": resultado[3],
                "fecha": str(resultado[4]),
                "hora": str(resultado[5]),
                "cantidad_personas": resultado[6],
                 "estado": resultado[7],
                "token": resultado[8],
                "qr_code": resultado[9],
                "fecha_creacion": str(resultado[10]) if resultado[10] else ""
            })
        else:
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener la reserva", "error": str(e)}), 500
    finally:
        cursor.close()


@reservas_bp.route('/', methods=['GET'])
def listar_todas_las_reservas():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reservas")
        resultado = cursor.fetchall()
        return jsonify([{
    "id_reserva": fila[0],
    "nombre": fila[1],
    "email": fila[2],
    "telefono": fila[3],
    "fecha": str(fila[4]),
    "hora": str(fila[5]),
    "cantidad_personas": fila[6],
    "estado": fila[7],
    "token": fila[8],
    "qr_code": fila[9],
    "fecha_creacion": str(fila[10]) if fila[10] else ""
} for fila in resultado])
    except Exception as e:
        return jsonify({"mensaje": "Error al listar las reservas", "error": str(e)}), 500
    finally:
        cursor.close()


@reservas_bp.route('/crear', methods=['POST'])
def crear_reserva():
    data = request.json
    email = data.get("email")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    fecha_recibida = data["fecha"] # Viene como '12/06/2026'
    hora_original = data["hora"]
    cantidad_personas = data["cantidad_personas"]

    # 🚀 PARSEO Y LIMPIEZA DE FECHA PARA MYSQL
    try:
        # Intentamos parsear el formato que está fallando (DD/MM/YYYY)
        fecha_objeto = datetime.strptime(fecha_recibida, "%d/%m/%Y")
        fecha = fecha_objeto.strftime("%Y-%m-%d") # Lo transforma a '2026-06-12'
    except ValueError:
        # Por si en algún momento vuelve a venir en formato ISO (YYYY-MM-DD)
        fecha = fecha_recibida

    # 🚀 BLINDAJE DE HORA (El que ya teníamos)
    if hora_original and len(hora_original) == 5:
        hora = f"{hora_original}:00"
    else:
        hora = hora_original

    conn = get_db()
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

        token = secrets.token_urlsafe(32)

        cursor.execute("SELECT COUNT(*) FROM reservas WHERE email = %s AND fecha = %s AND hora = %s AND estado != 'cancelada'", (email, fecha, hora))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            return jsonify({"mensaje": "Ya tenés una reserva para ese día y horario"}), 400

        # Insertar reserva básica
        cursor.execute(
            """INSERT INTO reservas 
            (nombre, email, telefono, fecha, hora, cantidad_personas, token) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (nombre, email, telefono, fecha, hora, cantidad_personas, token)
        )

        id_reserva = cursor.lastrowid

        # 🚨 Envolvemos QR y Email para que si fallan, sepamos qué pasó
        try:
            ruta_qr = generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token)
            cursor.execute(
                "UPDATE reservas SET qr_code = %s WHERE id_reserva = %s",
                (ruta_qr, id_reserva)
            )
            enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token, id_reserva)
        except Exception as e_externo:
            print(f"⚠️ Ojo: Falló el QR o el Email, pero intentaremos guardar igual: {e_externo}")

        conn.commit()
        return jsonify({"mensaje": "Reserva creada correctamente"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al crear la reserva", "error": str(e)}), 500
    finally:
        cursor.close()

@reservas_bp.route('/cancelar/<string:token>', methods=['GET'])
def cancelar_por_token(token):
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_reserva, estado FROM reservas WHERE token = %s",
            (token,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"mensaje": "El token de validacion no es valido"}), 400

        id_reserva, estado = resultado

        if estado == 'cancelada':
            return jsonify({"mensaje": "La reserva ya fue cancelada anteriormente"}), 400

        cursor.execute("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        return jsonify({"mensaje": "Reserva cancelada correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al cancelar la reserva", "error": str(e)}), 500
    finally:
        cursor.close()

        
@reservas_bp.route('/<int:id_reserva>/cancelar', methods=['PATCH'])
def modificar_reserva(id_reserva):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT estado FROM reservas WHERE id_reserva = %s", (id_reserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
        
        estado = resultado[0]
        if estado == 'cancelda':
            return jsonify({"mensaje": "La reserva ya fue cancelada anteriormente"}), 400
        cursor.execute("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        return jsonify({"mensaje": "Reserva cancelada correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje":" Error al cancelar la reserva", "error": str(e)}), 500
    finally:
        cursor.close()
        


@reservas_bp.route('/validar-qr', methods=['POST'])
def validar_qr():
    data = request.json
    id_reserva = data.get("id_reserva")
    qr_code = data.get("qr_code")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT qr_code, estado FROM reservas WHERE id_reserva = %s", (id_reserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"mensaje": "Reserva no encontrada"}), 404
        
        qr_code_almacenado, estado = resultado

        if estado == 'cancelada':
            return jsonify({"mensaje": "La reserva ha sido cancelada"}), 400

        if qr_code == qr_code_almacenado:
            cursor.execute(
                "UPDATE reservas SET estado = 'validada' WHERE id_reserva = %s",
                (id_reserva,)
            )
            conn.commit()
            return jsonify({"mensaje": "QR válido, acceso permitido"}), 200
        else:
            return jsonify({"mensaje": "QR inválido, acceso denegado"}), 400
    except Exception as e:
        return jsonify({"mensaje": "Error al validar el QR", "error": str(e)}), 500
    finally:
        cursor.close()


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