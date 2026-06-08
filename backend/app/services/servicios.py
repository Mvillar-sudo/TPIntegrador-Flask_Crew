from db import query_db, execute_db


def obtener_servicios():
    return query_db("""
        SELECT id,
               nombre,
               descripcion,
               activo,
               fecha_creacion
        FROM servicios
        ORDER BY nombre
    """)


def obtener_servicio_id(id_servicio):
    return query_db("""
        SELECT id,
               nombre,
               descripcion,
               activo,
               fecha_creacion
        FROM servicios
        WHERE id = %s
    """, (id_servicio,), one=True)


def crear_servicio_db(data):
    execute_db("""
        INSERT INTO servicios
        (nombre, descripcion)
        VALUES (%s, %s)
    """, (
        data['nombre'],
        data.get('descripcion')
    ))


def actualizar_servicio_db(id_servicio, data):

    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    activo = data.get('activo')

    return execute_db("""
        UPDATE servicios
        SET nombre = COALESCE(%s, nombre),
            descripcion = COALESCE(%s, descripcion),
            activo = COALESCE(%s, activo)
        WHERE id = %s
    """, (
        nombre,
        descripcion,
        activo,
        id_servicio
    ))


def eliminar_servicio_db(id_servicio):
    return execute_db(
        "DELETE FROM servicios WHERE id = %s",
        (id_servicio,)
    )