def validar_crear_plato(data):
    if not data:
        return "Body vacío"

    completar_campos = ["nombre_plato", "descripcion", "precio"]

    for campos in completar_campos:
        if campos not in data:
            return f"Falta el campo {campos}"

    if not isinstance(data["nombre_plato"], str) or not data["nombre_plato"].strip():
        return "Nombre inválido"

    if not isinstance(data["descripcion"], str):
        return "Descripción inválida"

    try:
        precio = float(data["precio"])
        if precio < 0:
            return "El precio no puede ser negativo"
    except:
        return "Precio inválido"

    return None


def validar_id_plato(id_plato):

    if id_plato <=0:
        return "id inválido"
    return None