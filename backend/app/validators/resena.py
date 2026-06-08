def validar_resena(data):
    if not data:
        return "No se enviaron datos"
    if 'comentario' not in data:
        return "El comentario es obligatorio"
    if 'calificacion' not in data:
        return "La calificación es obligatoria"
    if 'nombre_cliente' not in data:
        return "El nombre del cliente es obligatorio"

    comentario     = data['comentario']
    calificacion   = data['calificacion']
    nombre_cliente = data['nombre_cliente']

    if len(comentario.strip()) < 5:
        return "El comentario debe tener al menos 5 caracteres"
    if not isinstance(calificacion, int):
        return "La calificación debe ser numérica"
    if calificacion < 1 or calificacion > 5:
        return "La calificación debe estar entre 1 y 5"
    if len(nombre_cliente.strip()) < 2:
        return "El nombre del cliente debe tener al menos 2 caracteres"
    if len(nombre_cliente) > 100:
        return "El nombre del cliente no puede superar los 100 caracteres"

    return None