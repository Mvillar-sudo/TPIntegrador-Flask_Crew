from db import execute_db, query_db

def crear_plato_service(data):

    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    query = """
        INSERT INTO menu (nombre_plato, descripcion, precio)
        VALUES (%s, %s, %s)
    """
    args = (nombre, descripcion, precio)

    execute_db(query, args)
    return True

def obtener_menu_admin_service():
    query = "SELECT * FROM menu WHERE nombre_plato = %s;"
    platos = query_db(query)
    return platos

def obtener_menu_plato_service():
    query = "SELECT nombre_plato, descripcion, precio FROM menu WHERE estado = True"
    platos = query_db(query)
    return platos

def obtener_plato_service(id_plato):

    query = "SELECT * FROM menu WHERE id_plato = %s;"
    args = (id_plato,)

    plato = query_db(query, args)

    return plato

def actualizar_parcial_plato_service(id_plato, data):
    nombre_plato = data.get('nombre_plato'),
    descripcion = data.get('descripcion'),
    precio = data.get('precio'),
    query = """
            UPDATE menu 
            SET nombre_plato = COALESCE(%s, nombre_plato),
                descripcion = COALESCE(%s, descripcion),
                precio = COALESCE(%s, precio)
            WHERE id_plato = %s
        """
    args = (nombre_plato, descripcion, precio, id_plato)

    campos_actualizados = execute_db(query, args)
    if campos_actualizados == 0:
        return None

    return True

def cambiar_estado_plato_service(id_plato, estado):
    query = "UPDATE menu SET estado = %s WHERE id_plato = %s;"
    args = (estado, id_plato)

    filas_afectadas = execute_db(query, args)

    if filas_afectadas == 0:
        return None

    return True

def eliminar_plato_service(id_plato):
    query = "DELETE FROM menu WHERE id_plato = %s;"
    args = (id_plato,)

    filas_afectadas = execute_db(query, args)

    if filas_afectadas == 0:
        return None
    return True