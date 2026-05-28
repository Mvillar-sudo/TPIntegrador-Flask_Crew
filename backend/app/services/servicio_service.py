from db import execute_db, query_db

def post_servicio(datos):
    """Inserta un nuevo servicio extra en la base de datos.
    
    Args:
        datos (dict): Diccionario con 'nombre' (obligatorio) y 'descripcion' (opcional).
    
    Returns:
        dict: Mensaje de confirmación de creación.
    """
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    query = "INSERT INTO servicios (nombre, descripcion) VALUES (%s, %s)"
    args = (nombre, descripcion)
    execute_db(query, args)
    return {"mensaje": "Servicio creado con éxito"}

def get_servicio():
    """Obtiene todos los servicios extras ordenados por nombre.
    
    Returns:
        list: Lista de diccionarios con todos los servicios.
    """
    query = "SELECT * FROM servicios ORDER BY nombre"
    servicios = query_db(query)
    return servicios

def patch_servicio(id, datos):
    """Actualiza parcialmente un servicio extra existente.
    Usa COALESCE para conservar los valores anteriores si no se envía un campo.
    
    Args:
        id (int): ID del servicio a actualizar.
        datos (dict): Diccionario con los campos a actualizar ('nombre', 'descripcion', 'activo').
    
    Returns:
        dict: Mensaje de confirmación de actualización.
    """
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    activo = datos.get('activo')
    query = """UPDATE servicios SET nombre = COALESCE(%s, nombre), 
    descripcion = COALESCE(%s, descripcion), activo = COALESCE(%s, activo) WHERE id_servicio = %s"""
    args = (nombre, descripcion, activo, id)
    execute_db(query, args)
    return {"mensaje": "Servicio actualizado"}