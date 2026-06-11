from db import execute_db, query_db
from werkzeug.security import check_password_hash, generate_password_hash
import os
import datetime
import jwt
JWT_SECRET = os.getenv("JWT_SECRET", "clave_por_defecto_si_no_hay_env")

def generar_jwt(usuario_email):
    payload = {
        "sub": usuario_email,  # El 'subject' o dueño del token
        "iat": datetime.datetime.now(datetime.timezone.utc),  # Cuándo se creó
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)  # Cuándo expira
    }
    # Codificamos el token usando el algoritmo HS256
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def post_login(data):
    nombre = data["username"]
    password = data["password"]

    query = "SELECT email, password FROM usuarios WHERE email = %s AND activo = TRUE"
    resultado = query_db(query, (nombre,))  # Aprovechamos y dejamos la tupla fija

    if not resultado:
        return None

    user_db = resultado[0]

    if check_password_hash(user_db["password"], password):
        # ADAPTACIÓN JWT: Generamos el token si la contraseña es correcta
        token = generar_jwt(user_db["email"])

        # Devolvemos la estructura DTO (objeto limpio) + el Token para el Front
        return {
            "token": token,
            "usuario": {
                "email": user_db["email"]
            }
        }
    return None

def post_register(data):
    usuario = data["username"]
    password = data["password"]
    password_hash = generate_password_hash(password)

    query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
    nombre = usuario.split("@")[0]
    args = (nombre, usuario, password_hash)

    execute_db(query, args)
    return "Usuario registrado correctamente"
