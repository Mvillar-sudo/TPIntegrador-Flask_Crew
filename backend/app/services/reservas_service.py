from db import query_db, execute_db 

def obtener_total_reservas_pendientes():
    try:
        # 🌟 Ahora SÍ pasamos 'one=True' como tercer argumento explícito
        resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM reservas 
            WHERE estado = 'pendiente'
        """, one=True)
        
        print(f"DEBUG RESERVAS - Resultado crudo de la DB: {resultado}")

        # Como 'one=True' asegura un diccionario único: {'total': X}
        if resultado and isinstance(resultado, dict):
            return resultado.get('total', 0)
                
        return 0
    except Exception as e:
        print(f"⚠️ Error en reservas_service al contar pendientes: {e}")
        return 0