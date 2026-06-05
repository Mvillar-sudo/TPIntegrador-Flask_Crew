def validar_servicio(data, es_actualizacion=False):

    if not data:
        return "No se enviaron datos"

    if not es_actualizacion:

        if 'nombre' not in data:
            return "El nombre es obligatorio"

    if 'nombre' in data:

        nombre = data['nombre']

        if len(nombre.strip()) < 2:
            return "El nombre debe tener al menos 2 caracteres"

        if len(nombre) > 50:
            return "El nombre no puede superar los 50 caracteres"

    if 'descripcion' in data:

        if len(data['descripcion']) > 100:
            return "La descripción no puede superar los 100 caracteres"

    if 'activo' in data:

        if not isinstance(data['activo'], bool):
            return "El campo 'activo' debe ser un valor booleano"

    return None