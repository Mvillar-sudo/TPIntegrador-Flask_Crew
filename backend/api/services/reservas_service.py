from ..db import query_db, execute_db
from ..config import MAX_RESERVAS_POR_FRANJA
from ..validators.qr import generar_qr
from ..validators.email import enviar_email_reserva
import secrets

def obtener_reserva_service(id_reserva):
    resultado = query_db(
        "SELECT id_reserva, nombre, email, fecha, hora, cantidad_personas, estado, token_cancelacion, qr_code, fecha_creacion FROM reservas WHERE id_reserva = %s",
        (id_reserva,),
        one=True
    )
    if resultado:
        return {
            "id_reserva": resultado["id_reserva"],
            "nombre": resultado["nombre"],
            "email": resultado["email"],
            "fecha": str(resultado["fecha"]),
            "hora": str(resultado["hora"]),
            "cantidad_personas": resultado["cantidad_personas"],
            "estado": resultado["estado"],
            "token_cancelacion": resultado["token_cancelacion"],
            "qr_code": resultado["qr_code"],
            "fecha_creacion": str(resultado["fecha_creacion"]) if resultado["fecha_creacion"] else ""
        }
    return None

def listar_reservas_service():
    resultado = query_db(
        "SELECT id_reserva, nombre, email, fecha, hora, cantidad_personas, estado, token_cancelacion, qr_code, fecha_creacion FROM reservas"
    )
    return [{
        "id_reserva": fila["id_reserva"],
        "nombre": fila["nombre"],
        "email": fila["email"],
        "fecha": str(fila["fecha"]),
        "hora": str(fila["hora"]),
        "cantidad_personas": fila["cantidad_personas"],
        "estado": fila["estado"],
        "token_cancelacion": fila["token_cancelacion"],
        "qr_code": fila["qr_code"],
        "fecha_creacion": str(fila["fecha_creacion"]) if fila["fecha_creacion"] else ""
    } for fila in resultado]

def crear_reserva_service(data):
    email = data.get("email")
    nombre = data.get("nombre")
    fecha = data["fecha"]
    hora = data["hora"]
    cantidad_personas = data["cantidad_personas"]

    try:
        resultado = query_db("""
            SELECT COUNT(*) as total FROM reservas 
            WHERE fecha = %s AND hora = %s AND estado != 'cancelada'
        """, (fecha, hora), one=True)
        total_reservas = resultado["total"] if resultado is not None else 0

        if total_reservas >= MAX_RESERVAS_POR_FRANJA:
            return {"mensaje": {"mensaje": "No hay disponibilidad para esa fecha y hora"}, "estado": "sin_disponibilidad"}

        token_cancelacion = secrets.token_urlsafe(32)

        resultado = query_db(
            "SELECT COUNT(*) as total FROM reservas WHERE email = %s AND fecha = %s AND hora = %s AND estado != 'cancelada'",
            (email, fecha, hora),
            one=True
        )
        if resultado["total"] > 0:
            return {"mensaje": {"mensaje": "Ya tenés una reserva para ese día y horario"}, "estado": "duplicada"}

        execute_db(
            """INSERT INTO reservas 
            (nombre, email, fecha, hora, cantidad_personas, token_cancelacion) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (nombre, email, fecha, hora, cantidad_personas, token_cancelacion)
        )

        reserva_creada = query_db(
            "SELECT id_reserva FROM reservas WHERE token_cancelacion = %s",
            (token_cancelacion,),
            one=True
        )
        id_reserva = reserva_creada["id_reserva"]

        ruta_qr = generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion)
        execute_db(
            "UPDATE reservas SET qr_code = %s WHERE id_reserva = %s",
            (ruta_qr, id_reserva)
        )

        enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token_cancelacion, id_reserva, ruta_qr)

        return {"mensaje": {"mensaje": "Reserva creada correctamente"}, "estado": "creada"}

    except Exception as e:
        raise e

def cancelar_por_token_service(token):
    try:
        resultado = query_db(
            "SELECT id_reserva, estado FROM reservas WHERE token_cancelacion = %s",
            (token,),
            one=True
        )

        if resultado is None:
            return {"mensaje": {"mensaje": "El token de validacion no es valido"}, "estado": "token_invalido"}

        id_reserva = resultado["id_reserva"]
        estado = resultado["estado"]

        if estado == 'cancelada':
            return {"mensaje": {"mensaje": "La reserva ya fue cancelada anteriormente"}, "estado": "ya_cancelada"}

        execute_db("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        return {"mensaje": {"mensaje": "Reserva cancelada correctamente"}, "estado": "cancelada"}
    except Exception as e:
        raise e

def cancelar_reserva_service(id_reserva):
    try:
        resultado = query_db("SELECT estado FROM reservas WHERE id_reserva = %s", (id_reserva,), one=True)

        if resultado is None:
            return {"mensaje": {"mensaje": "Reserva no encontrada"}, "estado": "no_encontrada"}

        estado = resultado["estado"]
        if estado == 'cancelada':
            return {"mensaje": {"mensaje": "La reserva ya fue cancelada anteriormente"}, "estado": "ya_cancelada"}

        execute_db("UPDATE reservas SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        return {"mensaje": {"mensaje": "Reserva cancelada correctamente"}, "estado": "cancelada"}
    except Exception as e:
        raise e

def validar_qr_service(id_reserva, qr_code):
    try:
        resultado = query_db("SELECT qr_code, estado FROM reservas WHERE id_reserva = %s", (id_reserva,), one=True)

        if resultado is None:
            return {"estado": "no_encontrada"}

        qr_code_almacenado = resultado["qr_code"]
        estado = resultado["estado"]

        if estado == 'cancelada':
            return {"estado": "cancelada"}
        
        if estado == 'validada':
            return {"estado": "validada"}

        if qr_code != qr_code_almacenado:
            return {"estado": "qr_invalido"}

        execute_db(
            "UPDATE reservas SET estado = 'validada' WHERE id_reserva = %s",
            (id_reserva,)
        )
        return {"estado": "ok"}
    except Exception as e:
        raise e

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


def verificar_disponibilidad_service(fecha, hora):
    query = """
            SELECT COUNT(*) AS total \
            FROM reservas
            WHERE fecha = %s \
              AND hora = %s \
              AND estado != 'cancelada' \
            """
    resultado = query_db(query, (fecha, hora), one=True)
    total_reservas = resultado['total'] if resultado else 0

    disponibilidad = total_reservas < MAX_RESERVAS_POR_FRANJA

    return {
        "disponibilidad": disponibilidad,
        "reservas_actuales": total_reservas
    }
