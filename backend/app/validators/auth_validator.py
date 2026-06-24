def validar_login(data):
    if not data:
        return True, "No se recibieron datos" 

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return True, "Faltan campos obligatorios (usuario y password)" 
    return False, "Validación exitosa"