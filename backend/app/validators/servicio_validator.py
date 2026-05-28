def validar_servicio(datos, es_actualizacion=False):
    errores = []
    
    if not datos:
        return ["No se enviaron datos"]

    # 1. Validar Nombre
    if not es_actualizacion and 'nombre' not in datos:
        errores.append("El campo 'nombre' es obligatorio.")
    
    if 'nombre' in datos:
        nombre = datos.get('nombre')
        if not isinstance(nombre, str) or not nombre.strip():
            errores.append("El campo 'nombre' no puede estar vacío y debe ser texto.")
        elif len(nombre) > 50:
            errores.append("El campo 'nombre' no puede superar los 50 caracteres.")

    # 2. Validar Descripción 
    if 'descripcion' in datos:
        descripcion = datos.get('descripcion')
        if not isinstance(descripcion, str) or not descripcion.strip():
            errores.append("El campo 'descripcion' debe ser texto.")
        elif len(descripcion) > 100:
            errores.append("El campo 'descripcion' no puede superar los 100 caracteres.")

    # 3. Validar Activo
    if es_actualizacion and 'activo' in datos:
        activo = datos.get('activo')
        if not isinstance(activo, bool):
            errores.append("El campo 'activo' debe ser un valor booleano (true/false).")

    return errores
