from db import query_db, execute_db


def obtener_servicios():
    return query_db("""
        SELECT id_servicio,
               nombre,
               activo,
               fecha_creacion
        FROM servicios
        ORDER BY id_servicio
    """)


def obtener_servicio_id(id_servicio):
    return query_db("""
        SELECT id_servicio,
               nombre,
               activo,
               fecha_creacion
        FROM servicios
        WHERE id_servicio = %s
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
        WHERE id_servicio = %s
    """, (nombre, activo, id_servicio))


def eliminar_servicio_db(id_servicio):
    return execute_db(
        "DELETE FROM servicios WHERE id_servicio = %s",
        (id_servicio,)
    ) 
def obtener_total_servicios_activos():
    try:
        resultado = query_db("SELECT COUNT(*) as total FROM servicios WHERE activo = 1", one=True)
        
        if resultado and isinstance(resultado, dict): 
            return resultado.get('total', 0)
            
        return 0
    except Exception as e:
        print(f"⚠️ Error al contar servicios activos: {e}")
        return 0