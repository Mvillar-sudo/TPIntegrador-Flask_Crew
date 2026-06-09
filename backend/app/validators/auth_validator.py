def validar_login(data):
    if not data:
        return False, "No se recibieron datos"

    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return False, "Faltan campos obligatorios (usuario y password)"

    return True, None