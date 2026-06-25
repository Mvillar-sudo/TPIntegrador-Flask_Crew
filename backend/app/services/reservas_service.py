from db import query_db, execute_db, get_db
from config import MAX_RESERVAS_POR_FRANJA
from validators.qr import generar_qr
from validators.email import enviar_email_reserva
import secrets

def obtener_reserva_service(id_reserva):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_reserva, nombre, email, telefono, fecha, hora, cantidad_personas, estado, token_cancelacion, qr_code, fecha_creacion FROM reservas WHERE id_reserva = %s", (id_reserva,))
        resultado = cursor.fetchone()
        if resultado:
            return {
                "id_reserva": resultado[0],
                "nombre": resultado[1],
                "email": resultado[2],
                "telefono": resultado[3],
                "fecha": str(resultado[4]),
                "hora": str(resultado[5]),
                "cantidad_personas": resultado[6],
                "estado": resultado[7],
                "token_cancelacion": resultado[8],
                "qr_code": resultado[9],
                "fecha_creacion": str(resultado[10]) if resultado[10] else ""
            }
        return None
    finally:
        cursor.close()

def listar_reservas_service():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reservas")
        resultado = cursor.fetchall()
        return [{
            "id_reserva": fila[0],
            "nombre": fila[1],
            "email": fila[2],
            "telefono": fila[3],
            "fecha": str(fila[4]),
            "hora": str(fila[5]),
            "cantidad_personas": fila[6],
            "estado": fila[7],
            "token_cancelacion": fila[8],
            "qr_code": fila[9],
            "fecha_creacion": str(fila[10]) if fila[10] else ""
        } for fila in resultado]
    finally:
        cursor.close()

def crear_reserva_service(data):
    email = data.get("email")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    fecha = data["fecha"]
    hora = data["hora"]
    cantidad_personas = data["cantidad_personas"]

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM reservas 
            WHERE fecha = %s AND hora = %s AND estado != 'cancelada'
        """, (fecha, hora))
        resultado = cursor.fetchone()
        total_reservas = resultado[0] if resultado is not None else 0

        if total_reservas >= MAX_RESERVAS_POR_FRANJA:
            return {"mensaje": {"mensaje": "No hay disponibilidad para esa fecha y hora"}, "status": 400}

        token_cancelacion = secrets.token_urlsafe(32)

        cursor.execute("SELECT COUNT(*) FROM reservas WHERE email = %s AND fecha = %s AND hora = %s AND estado != 'cancelada'", (email, fecha, hora))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            return {"mensaje": {"mensaje": "Ya tenés una reserva para ese día y horario"}, "status": 400}

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

        enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token_cancelacion, id_reserva, ruta_qr)

        conn.commit()
        return {"mensaje": {"mensaje": "Reserva creada correctamente"}, "status": 201}

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def cancelar_por_token_service(token):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_reserva, estado FROM reservas WHERE token_cancelacion = %s",
            (token,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return {"mensaje": {"mensaje": "El token de validacion no es valido"}, "status": 400}

        id_reserva, estado = resultado

        if estado == 'cancelada':
            return {"mensaje": {"mensaje": "La reserva ya fue cancelada anteriormente"}, "status": 400}

        cursor.execute("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        return {"mensaje": {"mensaje": "Reserva cancelada correctamente"}, "status": 200}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def cancelar_reserva_service(id_reserva):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT estado FROM reservas WHERE id_reserva = %s", (id_reserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return {"mensaje": {"mensaje": "Reserva no encontrada"}, "status": 404}

        estado = resultado[0]
        if estado == 'cancelada':
            return {"mensaje": {"mensaje": "La reserva ya fue cancelada anteriormente"}, "status": 400}

        cursor.execute("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        return {"mensaje": {"mensaje": "Reserva cancelada correctamente"}, "status": 200}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def validar_qr_service(id_reserva, qr_code):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT qr_code, estado FROM reservas WHERE id_reserva = %s", (id_reserva,))
        resultado = cursor.fetchone()

        if resultado is None:
            return {"status": "no_encontrada"}

        qr_code_almacenado, estado = resultado

        if estado == 'cancelada':
            return {"status": "cancelada"}

        if qr_code != qr_code_almacenado:
            return {"status": "qr_invalido"}

        cursor.execute(
            "UPDATE reservas SET estado = 'validada' WHERE id_reserva = %s",
            (id_reserva,)
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def obtener_total_reservas_pendientes():
    try:
        resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM reservas 
            WHERE estado = 'pendiente'
        """, one=True)
        
        if resultado and isinstance(resultado, dict):
            return resultado.get('total', 0)
                
        return 0
    except Exception as e:
        print(f"⚠️ Error en reservas_service al contar pendientes: {e}")
        return 0