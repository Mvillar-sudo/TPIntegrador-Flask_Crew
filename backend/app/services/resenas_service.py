from db import query_db, execute_db

def obtener_resenas():
    return query_db("""
        SELECT id, comentario, calificacion, nombre_cliente, reserva_id, fecha_creacion
        FROM resenas
    """)

def obtener_resena_id(id_resena):
    return query_db("""
        SELECT id, comentario, calificacion, nombre_cliente, reserva_id, fecha_creacion
        FROM resenas
        WHERE id = %s
    """, (id_resena,), one=True)

def crear_resena_db(data):
    execute_db("""
        INSERT INTO resenas (comentario, calificacion, nombre_cliente, reserva_id)
        VALUES (%s, %s, %s, %s)
    """, (
        data['comentario'],
        data['calificacion'],
        data['nombre_cliente'],
        data.get('reserva_id')
    ))

def eliminar_resena_db(id_resena):
    return execute_db("DELETE FROM resenas WHERE id = %s", (id_resena,))

def obtener_cantidad_resenas():
    resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM menu 
            WHERE activo = 1
           """)
    if resultado and len(resultado) > 0:
        return resultado[0]['total']
    return 0