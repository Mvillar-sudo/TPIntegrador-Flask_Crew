from db import query_db, execute_db 

def obtener_total_reservas_pendientes():
    resultado = query_db("""
        SELECT COUNT(*) as total 
        FROM reservas 
        WHERE estado = pendiente
    """, one=True)
    return resultado['total'] if resultado else 0