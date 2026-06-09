from ..db import query_db, execute_db


def obtener_servicios():
    return query_db("""
        SELECT id,
               nombre,
               activo,
               fecha_creacion
        FROM servicios
        ORDER BY nombre
    """)


def obtener_servicio_id(id_servicio):
    return query_db("""
        SELECT id,
               nombre,
               activo,
               fecha_creacion
        FROM servicios
        WHERE id = %s
    """, (id_servicio,), one=True)


def crear_servicio_db(data):
    execute_db("""
        INSERT INTO servicios
        (nombre)
        VALUES (%s)
    """, (
        data['nombre'],
    ))


def actualizar_servicio_db(id_servicio, data):

    nombre = data.get('nombre')
    activo = 1 if data.get('activo') else 0


    return execute_db("""
        UPDATE servicios
        SET nombre = COALESCE(%s, nombre),
            activo = %s
        WHERE id = %s
    """, (nombre, activo, id_servicio))


def eliminar_servicio_db(id_servicio):
    return execute_db(
        "DELETE FROM servicios WHERE id = %s",
        (id_servicio,)
    ) 
def obtener_total_servicios_activos():
    resultado = query_db("""
        SELECT COUNT(*) as total 
        FROM servicios 
        WHERE activo = 1
    """, one=True)
    return resultado['total'] if resultado else 0