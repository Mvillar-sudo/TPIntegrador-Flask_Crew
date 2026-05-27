from db import execute_db, query_db

def post_servicio(datos):
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    query = "INSERT INTO servicios_extras (nombre, descripcion) VALUES (%s, %s)"
    args = (nombre, descripcion)
    execute_db(query, args)
    return {"mensaje": "Servicio creado con éxito"}

def get_servicio():
    query = "SELECT * FROM servicios_extras ORDER BY nombre"
    servicios = query_db(query)
    return servicios

def actualizar_servicio(id, datos):
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    activo = datos.get('activo')
    query = """UPDATE servicios_extras SET nombre = COALESCE(%s, nombre), 
    descripcion = COALESCE(%s, descripcion), activo = COALESCE(%s, activo) WHERE id = %s"""
    args = (nombre, descripcion, activo, id)
    execute_db(query, args)
    return {"mensaje": "Servicio actualizado"}