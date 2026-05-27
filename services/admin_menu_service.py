from db import get_connection

def crear_plato_service(data):

    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    conn = get_connection()
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

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu")
    platos = cursor.fetchall()

    cursor.close()
    conn.close()

    return platos


def obtener_plato_service(id_plato):

    conn = get_connection()
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

    conn = get_connection()
    cursor = conn.cursor()

    campos_actualizados = 0

    if "nombre_plato" in data:
        cursor.execute(
            "UPDATE menu SET nombre_plato = %s WHERE id_plato = %s",
            (data["nombre_plato"], id_plato)
        )
        campos_actualizados += cursor.rowcount

    if "descripcion" in data:
        cursor.execute(
            "UPDATE menu SET descripcion = %s WHERE id_plato = %s",
            (data["descripcion"], id_plato)
        )
        campos_actualizados += cursor.rowcount

    if "precio" in data:
        cursor.execute(
            "UPDATE menu SET precio = %s WHERE id_plato = %s",
            (data["precio"], id_plato)
        )
        campos_actualizados += cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    if campos_actualizados == 0:
        return None

    return True



def cambiar_estado_plato_service(id_plato, estado):

    conn = get_connection()
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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM menu WHERE id_plato = %s",
        (id_plato,)
    )

    conn.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return None

    return True