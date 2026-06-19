from db import query_db, execute_db

def obtener_resenas():
    return query_db("""
        SELECT id_resena AS id, comentario, calificacion, nombre_cliente, fecha_creacion
        FROM resenas
        ORDER BY fecha_creacion DESC
    """)

def obtener_resena_id(id_resena):
    return query_db("""
        SELECT id_resena AS id, comentario, calificacion, nombre_cliente, fecha_creacion
        FROM resenas
        WHERE id_resena = %s
    """, (id_resena,), one=True)

def crear_resena_db(data):
    execute_db("""
        INSERT INTO resenas (comentario, calificacion, nombre_cliente)
        VALUES (%s, %s, %s)
    """, (
        data['comentario'],
        data['calificacion'],
        data['nombre_cliente'],
    ))

def eliminar_resena_db(id_resena):
    return execute_db("DELETE FROM resenas WHERE id_resena = %s", (id_resena,))