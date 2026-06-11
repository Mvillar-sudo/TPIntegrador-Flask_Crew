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
    query = "SELECT * FROM menu;"
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
    """Actualiza un plato en la base de datos limpiando cualquier dato corrupto."""
    
    # 🚀 EXTRACCIÓN LIMPIA Y SEGURA (Evitamos que se cuelen tuplas accidentales)
    # Si por algún motivo venía como tupla o lista, extraemos solo el primer valor [0]
    nombre_plato = data.get("nombre_plato")
    if isinstance(nombre_plato, (tuple, list)): nombre_plato = nombre_plato[0]
        
    descripcion = data.get("descripcion")
    if isinstance(descripcion, (tuple, list)): descripcion = descripcion[0]
        
    precio = data.get("precio")
    if isinstance(precio, (tuple, list)): precio = precio[0]
        
    estado = data.get("estado")
    if isinstance(estado, (tuple, list)): estado = estado[0]

    imagen = data.get("imagen")
    if isinstance(imagen, (tuple, list)): imagen = imagen[0]

    # Armamos la query dinámica o estática según uses COALESCE
    query = """
        UPDATE menu 
        SET nombre_plato = COALESCE(%s, nombre_plato),
            descripcion = COALESCE(%s, descripcion),
            precio = COALESCE(%s, precio),
            estado = COALESCE(%s, estado),
            imagen = COALESCE(%s, imagen)
        WHERE id_plato = %s
    """
    
    # 🚀 Forzamos la conversión estricta de tipos de datos en la tupla final
    args = (
        str(nombre_plato) if nombre_plato is not None else None,
        str(descripcion) if descripcion is not None else None,
        float(precio) if precio is not None else None,
        int(estado) if estado is not None else None,
        str(imagen) if imagen is not None else None,
        int(id_plato)
    )

    # Ejecutamos en la base de datos
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

def obtener_total_platos_activos():
    resultado = query_db("SELECT COUNT(*) as total FROM menu WHERE activo = 1", one=True)
    if resultado:
        if isinstance(resultado, dict): return resultado.get('total', 0)
        return resultado[0]
    return 0