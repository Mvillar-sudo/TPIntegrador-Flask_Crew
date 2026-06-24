from db import query_db, execute_db


def obtener_resenas():
    return query_db("""
        SELECT *
        FROM resenas
        ORDER BY calificacion DESC
    """)


def obtener_resena_id(id_resena):
    return query_db("""
        SELECT id_resena AS id, comentario, calificacion, nombre_cliente, email, fecha_creacion
        FROM resenas
        WHERE id_resena = %s
    """, (id_resena,), one=True)


def crear_resena_db(data):
    return execute_db("""
        INSERT INTO resenas (comentario, calificacion, nombre_cliente, email)
        VALUES (%s, %s, %s, %s)
    """, (data['comentario'], data['calificacion'], data['nombre_cliente'], data['email']))


def eliminar_resena_db(id_resena):
    return execute_db("DELETE FROM resenas WHERE id_resena = %s", (id_resena,))

def obtener_total_resenas_positivas():
    try:
        resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM resenas 
            WHERE calificacion > 2
        """)
        
        if resultado and isinstance(resultado, list):
            primera_fila = resultado[0]
            return primera_fila.get('total', 0)
                
        return 0
    except Exception as e:
        print(f"⚠️ Error en resenas_service al contar positivas: {e}")
        return 0 

def obtener_total_resenas_negativas():
    try:
        resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM resenas 
            WHERE calificacion < 3
        """)
        
        if resultado and isinstance(resultado, list):
            primera_fila = resultado[0]
            return primera_fila.get('total', 0)
                
        return 0
    except Exception as e:
        print(f"⚠️ Error en resenas_service al contar negativas: {e}")
        return 0