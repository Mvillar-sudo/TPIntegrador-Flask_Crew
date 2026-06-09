from ..db import get_db, query_db

def crear_plato_service(data):

    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO menu (nombre_plato, descripcion, precio)
        VALUES (%s, %s, %s)
    """, (nombre, descripcion, precio))

    conn.commit()
    cursor.close()
    conn.close()

    return True


def obtener_menu_admin_service():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu")
    platos = cursor.fetchall()

    cursor.close()
    conn.close()

    return platos


def obtener_plato_service(id_plato):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM menu WHERE id_plato = %s",
        (id_plato,)
    )

    plato = cursor.fetchone()

    cursor.close()
    conn.close()

    return plato



def actualizar_parcial_plato_service(id_plato, data):
    conn = get_db()
    cursor = conn.cursor()

    campos_permitidos = ["nombre_plato", "descripcion", "precio", "estado"]
    query_parts = []
    valores = []

    for campo in campos_permitidos:
        if campo in data:
            query_parts.append(f"{campo} = %s")
            valores.append(data[campo])

    if not query_parts:
        cursor.close()
        conn.close()
        return True 

    sql = f"UPDATE menu SET {', '.join(query_parts)} WHERE id_plato = %s"
    valores.append(id_plato)

    cursor.execute(sql, tuple(valores))
    conn.commit()

    cursor.close()
    conn.close()

    return True



def cambiar_estado_plato_service(id_plato, estado):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE menu SET estado = %s WHERE id_plato = %s",
        (estado, id_plato)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return None

    return True



def eliminar_plato_service(id_plato):
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM menu WHERE id_plato = %s",
        (id_plato,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas_afectadas > 0 

def obtener_total_platos_activos():
    resultado = query_db("""
        SELECT COUNT(*) as total 
        FROM menu 
        WHERE estado = 1
    """, one=True)
    return resultado['total'] if resultado else 0