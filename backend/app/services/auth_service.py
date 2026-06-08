from db import execute_db, query_db
from werkzeug.security import check_password_hash, generate_password_hash

def post_login(data):
    usuario = data["usuario"]
    password = data["password"]
    query = "SELECT email, password FROM usuarios WHERE email = %s AND activo = TRUE"
    resultado = query_db(query, usuario)

    if not resultado:
        return None  # El usuario no existe

    user_db = resultado[0]

    if check_password_hash(user_db["password"], password):
        return {"usuario": user_db["email"]}

    return None

def post_register(data):
    usuario = data["usuario"]
    password = data["password"]
    password_hash = generate_password_hash(password)

    query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
    nombre = usuario.split("@")[0]
    args = (nombre, usuario, password_hash)

    execute_db(query, args)
    return "Usuario registrado correctamente"
