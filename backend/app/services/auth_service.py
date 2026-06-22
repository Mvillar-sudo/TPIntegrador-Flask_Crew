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
    email_usuario = data["email"] 
    password = data["password"]

    query = "SELECT email, password FROM usuarios WHERE email = %s AND activo = TRUE"
    resultado = query_db(query, (email_usuario,))

    if not resultado:
        return None

    user_db = resultado[0]

    if check_password_hash(user_db["password"], password):
        token = generar_jwt(user_db["email"])
        return {
            "token": token,
            "usuario": {
                "email": user_db["email"]
            }
        }
    return None

def post_register(data):
    email_usuario = data["email"] 
    password = data["password"]
    password_hash = generate_password_hash(password)

    query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
    nombre = data.get("nombre") or email_usuario.split("@")[0] 
    args = (nombre, email_usuario, password_hash)

    execute_db(query, args)
    return "Usuario registrado correctamente"
