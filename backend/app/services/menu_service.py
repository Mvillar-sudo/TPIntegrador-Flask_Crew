from db import execute_db, query_db

def crear_plato_service(data):

    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]
    imagen = data['imagen']

    query = """
        INSERT INTO menu (nombre_plato, descripcion, precio, imagen)
        VALUES (%s, %s, %s, %s)
    """
    args = (nombre, descripcion, precio, imagen)

    execute_db(query, args)
    return True

def obtener_menu_admin_service():
    query = "SELECT * FROM menu"
    platos = query_db(query)
    if platos:
        for plato in platos:
            if "precio" in plato and plato["precio"] is not None:
                plato["precio"] = float(plato["precio"])
    return platos

def obtener_menu_plato_service():
    query = "SELECT nombre_plato, descripcion, precio, imagen FROM menu WHERE activo = True"
    platos = query_db(query)
    if platos:
        for plato in platos:
            if "precio" in plato and plato["precio"] is not None:
                plato["precio"] = float(plato["precio"])
    return platos

def obtener_plato_service(id_plato):

    query = "SELECT * FROM menu WHERE id_plato = %s;"
    args = (id_plato,)

    plato = query_db(query, args)

    return plato

def actualizar_parcial_plato_service(id_plato, data):
    nombre_plato = data.get('nombre_plato')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    imagen = data.get('imagen')
    query = """
            UPDATE menu 
            SET nombre_plato = COALESCE(%s, nombre_plato),
                descripcion = COALESCE(%s, descripcion),
                precio = COALESCE(%s, precio),
                imagen = COALESCE(%s, imagen)
            WHERE id_plato = %s
        """
    args = (nombre_plato, descripcion, precio, imagen, id_plato)

    execute_db(query, args)

    return True

def cambiar_estado_plato_service(id_plato, estado):
    query = "UPDATE menu SET activo = %s WHERE id_plato = %s;"
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


def obtener_total_platos_activos_service():
    resultado = query_db("""
           SELECT COUNT(*) as total 
           FROM menu 
           WHERE activo = 1
       """)
    if resultado and len(resultado) > 0:
        return resultado[0]['total']
    return 0