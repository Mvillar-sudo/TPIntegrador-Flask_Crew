def validar_crear_servicio(datos):
    errores = []
    
    if not datos:
        return ["No se enviaron datos"]

    # Validación de nombre (Obligatorio)
    nombre = datos.get('nombre')
    if not nombre or not isinstance(nombre, str) or not nombre.strip():
        errores.append("El campo 'nombre' es obligatorio y debe ser texto.")
    elif len(nombre) > 100:
        errores.append("El campo 'nombre' no puede superar los 100 caracteres.")
        
    return errores

def validar_actualizar_servicio(datos):
    errores = []
    
    if not datos:
        return ["No se enviaron datos"]

    # Validación de nombre
    if 'nombre' in datos:
        nombre = datos.get('nombre')
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            errores.append("El campo 'nombre' no puede estar vacío y debe ser texto.")
        elif len(nombre) > 100:
            errores.append("El campo 'nombre' no puede superar los 100 caracteres.")

    # Validación de estado activo
    if 'activo' in datos:
        activo = datos.get('activo')
        if not isinstance(activo, bool):
            errores.append("El campo 'activo' debe ser un valor booleano (true/false).")

    return errores
